import { Component, DestroyRef, effect, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { finalize, forkJoin, Subject, takeUntil } from 'rxjs';
import { PersonalService, UserLicense, LicenseInput } from '../services/personal.service';
import { Catalog, RegulationsService } from '../services/regulations.service';
import { apiErrorMessage } from '../services/api-error';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-licenses',
  imports: [CommonModule, FormsModule],
  templateUrl: './licenses.html',
  styleUrls: ['./licenses.css', '../personal-forms.css']
})
export class Licenses implements OnInit {
  private readonly personal = inject(PersonalService);
  private readonly regulations = inject(RegulationsService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly auth = inject(AuthService);
  private readonly ownerChanged = new Subject<void>();
  readonly myLicenses = signal<UserLicense[]>([]);
  readonly loading = signal(true);
  readonly busy = signal(false);
  readonly error = signal('');
  readonly message = signal('');
  catalog: Catalog | null = null;
  editingId: number | undefined;
  form: LicenseInput = this.blankForm();
  ready = false;
  readonly statuses = [
    { value: 'unknown', label: 'Unknown / not checked' }, { value: 'held', label: 'Held (self-reported)' },
    { value: 'not_held', label: 'Not held' }, { value: 'expired', label: 'Expired' }
  ];
  readonly buyLinks = [
    { name: 'FWC Official License Portal', url: 'https://gooutdoorsflorida.com/' },
    { name: 'Federal Duck Stamp', url: 'https://www.fws.gov/birds/get-involved/duck-stamp/buy-duck-stamp.php' },
    { name: 'WMA Brochures & Quota Permits', url: 'https://myfwc.com/hunting/wma-brochures/' }
  ];

  constructor() {
    let ownerId = this.auth.currentUser()?.id;
    effect(() => {
      const nextOwnerId = this.auth.currentUser()?.id;
      if (ownerId === nextOwnerId) return;
      ownerId = nextOwnerId;
      this.ownerChanged.next();
      this.myLicenses.set([]);
      this.cancelEdit();
      this.ready = false;
      this.message.set('');
      if (nextOwnerId !== undefined) this.load();
      else { this.loading.set(false); this.error.set('Your session ended. Sign in to view your saved information.'); }
    });
  }

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading.set(true);
    this.error.set('');
    forkJoin({ licenses: this.personal.licenses(), catalog: this.regulations.catalog() }).pipe(
      finalize(() => this.loading.set(false)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: data => { this.myLicenses.set(data.licenses); this.catalog = data.catalog; this.ready = true; },
      error: error => this.error.set(apiErrorMessage(error, 'Unable to load your licenses. Please try again.'))
    });
  }

  choosePermit(): void {
    const name = this.catalog?.license_permits?.find(item => item.id === this.form.permit)?.name;
    if (name) this.form.name = name;
  }

  statusLabel(status: string): string { return this.statuses.find(item => item.value === status)?.label || status; }

  saveLicense(): void {
    if (!this.ready || this.busy() || !this.form.name.trim()) return;
    this.busy.set(true);
    this.error.set('');
    this.message.set('');
    const value = { ...this.form, name: this.form.name.trim(), valid_from: this.form.valid_from || null, expires_on: this.form.expires_on || null };
    this.personal.saveLicense(value, this.editingId).pipe(
      finalize(() => this.busy.set(false)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: license => {
        this.myLicenses.update(items => [license, ...items.filter(item => item.id !== license.id)]);
        this.cancelEdit();
        this.message.set('License status saved to your account.');
      },
      error: error => this.error.set(apiErrorMessage(error, 'Unable to save this license. Your entries are still here; try again.'))
    });
  }

  editLicense(license: UserLicense): void {
    if (this.busy()) return;
    this.editingId = license.id;
    this.form = { permit: license.permit, name: license.name, status: license.status, valid_from: license.valid_from, expires_on: license.expires_on, notes: license.notes };
    this.message.set('Editing license status. Use the form above to save your changes.');
  }

  cancelEdit(): void { this.editingId = undefined; this.form = this.blankForm(); }

  deleteLicense(license: UserLicense): void {
    if (this.busy()) return;
    this.busy.set(true);
    this.error.set('');
    this.personal.deleteLicense(license.id).pipe(
      finalize(() => this.busy.set(false)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: () => {
        this.myLicenses.update(items => items.filter(item => item.id !== license.id));
        if (this.editingId === license.id) this.cancelEdit();
        this.message.set('License status deleted.');
      },
      error: error => this.error.set(apiErrorMessage(error, 'Unable to delete this license. Please try again.'))
    });
  }

  private blankForm(): LicenseInput { return { permit: null, name: '', status: 'unknown', valid_from: null, expires_on: null, notes: '' }; }
}
