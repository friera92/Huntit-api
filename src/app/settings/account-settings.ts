import { CommonModule } from '@angular/common';
import { Component, DestroyRef, effect, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule, NgForm } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { finalize, Subject, takeUntil } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { apiErrorMessage } from '../services/api-error';
import { PersonalService } from '../services/personal.service';

@Component({
  selector: 'app-account-settings', imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './account-settings.html', styleUrls: ['../auth/account.css', './account-settings.css']
})
export class AccountSettings {
  readonly auth = inject(AuthService);
  private readonly personal = inject(PersonalService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly ownerChanged = new Subject<void>();
  readonly passwordPending = signal(false);
  readonly dataPending = signal(false);
  readonly passwordError = signal('');
  readonly passwordSuccess = signal('');
  readonly dataError = signal('');
  readonly dataSuccess = signal('');
  currentPassword = '';
  newPassword = '';
  newPasswordConfirm = '';
  clearPreferences = false;
  clearSavedSearches = false;
  clearLicenses = false;
  archiveHarvests = false;
  confirmation = '';

  constructor() {
    let ownerId = this.auth.currentUser()?.id;
    effect(() => {
      const nextOwnerId = this.auth.currentUser()?.id;
      if (ownerId === nextOwnerId) return;
      ownerId = nextOwnerId;
      this.ownerChanged.next();
      this.currentPassword = ''; this.newPassword = ''; this.newPasswordConfirm = '';
      this.clearPreferences = false; this.clearSavedSearches = false; this.clearLicenses = false;
      this.archiveHarvests = false; this.confirmation = '';
      this.passwordError.set(''); this.passwordSuccess.set(''); this.dataError.set(''); this.dataSuccess.set('');
    });
  }

  changePassword(form: NgForm): void {
    if (form.invalid || this.passwordPending()) return;
    this.passwordError.set(''); this.passwordSuccess.set('');
    if (this.newPassword !== this.newPasswordConfirm) { this.passwordError.set('Passwords must match.'); return; }
    this.passwordPending.set(true);
    this.auth.changePassword({ current_password: this.currentPassword, new_password: this.newPassword,
      new_password_confirm: this.newPasswordConfirm }).pipe(finalize(() => this.passwordPending.set(false)),
      takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)).subscribe({
      next: response => { this.passwordPending.set(false); form.resetForm(); this.passwordSuccess.set(response.detail); },
      error: error => { this.passwordPending.set(false); this.currentPassword = ''; this.newPassword = ''; this.newPasswordConfirm = '';
        this.passwordError.set(apiErrorMessage(error, 'Unable to change your password. Please try again.')); }
    });
  }

  exportData(): void {
    if (this.dataPending()) return;
    this.dataPending.set(true); this.dataError.set(''); this.dataSuccess.set('');
    this.personal.exportData().pipe(finalize(() => this.dataPending.set(false)),
      takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)).subscribe({
      next: data => {
        this.dataPending.set(false);
        const url = URL.createObjectURL(data);
        const anchor = document.createElement('a'); anchor.href = url; anchor.download = 'huntit-personal-data.json'; anchor.click();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
        this.dataSuccess.set('Your personal-data export is ready.');
      },
      error: error => { this.dataPending.set(false); this.dataError.set(apiErrorMessage(error, 'Unable to export your data.')); }
    });
  }

  resetData(): void {
    if (this.dataPending() || this.confirmation !== 'RESET MY DATA' || !this.hasSelection) return;
    this.dataPending.set(true); this.dataError.set(''); this.dataSuccess.set('');
    this.personal.resetData({
      preferences: this.clearPreferences, saved_searches: this.clearSavedSearches, licenses: this.clearLicenses,
      harvests: this.archiveHarvests ? 'archive' : 'keep', confirmation: this.confirmation,
    }).pipe(finalize(() => this.dataPending.set(false)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)).subscribe({
      next: () => { this.dataPending.set(false); this.confirmation = ''; this.clearPreferences = false; this.clearSavedSearches = false;
        this.clearLicenses = false; this.archiveHarvests = false;
        this.dataSuccess.set('Selected saved information was cleared. Archived harvests can be restored from Harvest Log.'); },
      error: error => { this.dataPending.set(false); this.dataError.set(apiErrorMessage(error, 'Unable to reset your saved information.')); }
    });
  }

  get hasSelection(): boolean { return this.clearPreferences || this.clearSavedSearches || this.clearLicenses || this.archiveHarvests; }
}
