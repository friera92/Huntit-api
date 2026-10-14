import { Component, DestroyRef, effect, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { finalize, forkJoin, Subject, takeUntil } from 'rxjs';
import { Harvest, HarvestInput, PersonalService } from '../services/personal.service';
import { Catalog, RegulationsService, Species } from '../services/regulations.service';
import { apiErrorMessage } from '../services/api-error';
import { AuthService } from '../services/auth.service';

@Component({
  imports: [CommonModule, FormsModule],
  selector: 'app-log',
  styleUrl: './log.css',
  templateUrl: './log.html',
})
export class Log implements OnInit {
  private readonly personal = inject(PersonalService);
  private readonly regulations = inject(RegulationsService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly auth = inject(AuthService);
  private readonly ownerChanged = new Subject<void>();
  readonly recentHarvests = signal<Harvest[]>([]);
  readonly loading = signal(true);
  readonly busy = signal(false);
  readonly error = signal('');
  readonly message = signal('');
  readonly today = this.localDate();
  catalog: Catalog | null = null;
  species: Species[] = [];
  form = this.blankForm();
  editingId: number | undefined;
  showArchived = false;
  confirmingDelete: number | null = null;
  ready = false;

  constructor() {
    let ownerId = this.auth.currentUser()?.id;
    effect(() => {
      const nextOwnerId = this.auth.currentUser()?.id;
      if (ownerId === nextOwnerId) return;
      ownerId = nextOwnerId;
      this.ownerChanged.next();
      this.recentHarvests.set([]);
      this.cancelEdit();
      this.confirmingDelete = null;
      this.showArchived = false;
      this.ready = false;
      this.message.set('');
      if (nextOwnerId !== undefined) this.load();
      else { this.loading.set(false); this.error.set('Your session ended. Sign in to view your saved information.'); }
    });
  }

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading.set(true);
    this.ready = false;
    this.recentHarvests.set([]);
    this.error.set('');
    forkJoin({ harvests: this.personal.harvests(this.showArchived), catalog: this.regulations.catalog(), species: this.regulations.species() }).pipe(
      finalize(() => this.loading.set(false)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: data => { this.recentHarvests.set(data.harvests); this.catalog = data.catalog; this.species = data.species; this.ready = true; },
      error: error => this.error.set(apiErrorMessage(error, 'Unable to load your harvest log. Please try again.'))
    });
  }

  toggleArchive(): void {
    if (this.loading() || this.busy()) return;
    this.showArchived = !this.showArchived;
    this.cancelEdit();
    this.confirmingDelete = null;
    this.message.set('');
    this.load();
  }

  saveHarvest(): void {
    if (!this.ready || this.busy() || !this.form.species || !this.form.harvest_date || (!this.form.managed_area && !this.form.location.trim())) return;
    this.busy.set(true);
    this.error.set('');
    this.message.set('');
    const value: HarvestInput = { ...this.form, species: this.form.species, location: this.form.location.trim() };
    this.personal.saveHarvest(value, this.editingId).pipe(
      finalize(() => this.busy.set(false)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: harvest => {
        this.recentHarvests.update(items => [harvest, ...items.filter(item => item.id !== harvest.id)]);
        this.cancelEdit();
        this.message.set('Harvest saved to your private account log.');
      },
      error: error => this.error.set(apiErrorMessage(error, 'Unable to save your harvest. Your entries are still here; try again.'))
    });
  }

  editHarvest(harvest: Harvest): void {
    if (this.busy() || this.showArchived) return;
    this.editingId = harvest.id;
    this.form = { species: harvest.species, harvest_date: harvest.harvest_date, managed_area: harvest.managed_area, location: harvest.location, quantity: harvest.quantity, notes: harvest.notes };
    this.message.set('Editing harvest. Use the form above to save your changes.');
  }

  cancelEdit(): void { this.editingId = undefined; this.form = this.blankForm(); }

  archiveHarvest(harvest: Harvest, restore = false): void {
    if (this.busy()) return;
    this.busy.set(true);
    this.error.set('');
    const request = restore ? this.personal.restoreHarvest(harvest.id) : this.personal.archiveHarvest(harvest.id);
    request.pipe(finalize(() => this.busy.set(false)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)).subscribe({
      next: () => {
        this.recentHarvests.update(items => items.filter(item => item.id !== harvest.id));
        if (this.editingId === harvest.id) this.cancelEdit();
        this.message.set(restore ? 'Harvest restored to your active log.' : 'Harvest archived. You can restore it from Archived Harvests.');
      },
      error: error => this.error.set(apiErrorMessage(error, 'Unable to update this harvest. Please try again.'))
    });
  }

  deleteHarvest(harvest: Harvest): void {
    if (this.busy() || this.confirmingDelete !== harvest.id) return;
    this.busy.set(true);
    this.error.set('');
    this.personal.deleteHarvest(harvest.id).pipe(
      finalize(() => this.busy.set(false)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: () => {
        this.recentHarvests.update(items => items.filter(item => item.id !== harvest.id));
        if (this.editingId === harvest.id) this.cancelEdit();
        this.confirmingDelete = null;
        this.message.set('Harvest permanently deleted.');
      },
      error: error => this.error.set(apiErrorMessage(error, 'Unable to delete this harvest. Please try again.'))
    });
  }

  private blankForm(): Omit<HarvestInput, 'species'> & { species: number | null } {
    return { species: null, harvest_date: '', managed_area: null, location: '', quantity: 1, notes: '' };
  }
  private localDate(): string {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
  }
}
