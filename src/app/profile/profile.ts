import { Component, computed, DestroyRef, effect, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { finalize, forkJoin, Subject, takeUntil } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { PersonalService, Preferences, SavedSearch, savedSearchQuery } from '../services/personal.service';
import { Catalog, RegulationsService, Species } from '../services/regulations.service';
import { apiErrorMessage } from '../services/api-error';

@Component({
  imports: [CommonModule, FormsModule, RouterModule],
  selector: 'app-profile',
  styleUrls: ['./profile.css', '../personal-forms.css'],
  templateUrl: './profile.html',
})
export class Profile implements OnInit {
  private readonly personal = inject(PersonalService);
  private readonly regulations = inject(RegulationsService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly ownerChanged = new Subject<void>();
  readonly user = inject(AuthService).currentUser;
  readonly displayName = computed(() => {
    const user = this.user();
    return user ? [user.first_name, user.last_name].filter(Boolean).join(' ') || user.username : '';
  });
  readonly loading = signal(true);
  readonly saving = signal(false);
  readonly busySearch = signal<number | null>(null);
  readonly error = signal('');
  readonly message = signal('');
  readonly savedSearches = signal<SavedSearch[]>([]);
  readonly savedSearchQuery = savedSearchQuery;
  catalog: Catalog | null = null;
  species: Species[] = [];
  preferences: Preferences = { species: [], managed_areas: [], zones: [] };
  editingSearch: number | null = null;
  searchTitle = '';
  ready = false;

  constructor() {
    let ownerId = this.user()?.id;
    effect(() => {
      const nextOwnerId = this.user()?.id;
      if (ownerId === nextOwnerId) return;
      ownerId = nextOwnerId;
      this.ownerChanged.next();
      this.savedSearches.set([]);
      this.preferences = { species: [], managed_areas: [], zones: [] };
      this.ready = false;
      this.editingSearch = null;
      this.searchTitle = '';
      this.message.set('');
      if (nextOwnerId !== undefined) this.load();
      else { this.loading.set(false); this.error.set('Your session ended. Sign in to view your saved information.'); }
    });
  }

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading.set(true);
    this.error.set('');
    forkJoin({
      preferences: this.personal.preferences(), searches: this.personal.savedSearches(),
      catalog: this.regulations.catalog(), species: this.regulations.species()
    }).pipe(finalize(() => this.loading.set(false)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)).subscribe({
      next: data => {
        this.preferences = data.preferences;
        this.savedSearches.set(data.searches);
        this.catalog = data.catalog;
        this.species = data.species;
        this.ready = true;
      },
      error: error => this.error.set(apiErrorMessage(error, 'Unable to load your profile. Please try again.'))
    });
  }

  savePreferences(): void {
    if (!this.ready || this.saving()) return;
    this.saving.set(true);
    this.error.set('');
    this.message.set('');
    this.personal.savePreferences(this.preferences).pipe(
      finalize(() => this.saving.set(false)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: preferences => { this.preferences = preferences; this.message.set('Preferences saved to your account.'); },
      error: error => this.error.set(apiErrorMessage(error, 'Unable to save preferences. Your selections are still here; try again.'))
    });
  }

  editSearch(search: SavedSearch): void { this.editingSearch = search.id; this.searchTitle = search.title; }

  renameSearch(search: SavedSearch): void {
    if (this.busySearch() !== null || !this.searchTitle.trim()) return;
    this.busySearch.set(search.id);
    this.error.set('');
    this.personal.renameSearch(search.id, this.searchTitle.trim()).pipe(
      finalize(() => this.busySearch.set(null)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: updated => {
        this.savedSearches.update(items => items.map(item => item.id === search.id ? updated : item));
        this.editingSearch = null;
        this.message.set('Saved search renamed.');
      },
      error: error => this.error.set(apiErrorMessage(error, 'Unable to rename this search. Please try again.'))
    });
  }

  deleteSearch(search: SavedSearch): void {
    if (this.busySearch() !== null) return;
    this.busySearch.set(search.id);
    this.error.set('');
    this.personal.deleteSearch(search.id).pipe(
      finalize(() => this.busySearch.set(null)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: () => {
        this.savedSearches.update(items => items.filter(item => item.id !== search.id));
        if (this.editingSearch === search.id) this.editingSearch = null;
        this.message.set('Saved search deleted.');
      },
      error: error => this.error.set(apiErrorMessage(error, 'Unable to delete this search. Please try again.'))
    });
  }
}
