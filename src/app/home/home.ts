import { Component, DestroyRef, effect, ElementRef, inject, OnInit, signal, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterModule, Router } from '@angular/router';
import { forkJoin, Subscription } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Catalog, regulatoryAreasFor, RegulationsService, SearchQuery, Species } from '../services/regulations.service';
import { apiErrorMessage } from '../services/api-error';
import { AuthService } from '../services/auth.service';
import { PersonalService, Preferences } from '../services/personal.service';

@Component({
  imports: [CommonModule, FormsModule, RouterModule],
  selector: 'app-home',
  styleUrl: './home.css',
  templateUrl: './home.html',
})
export class Home implements OnInit {
  private readonly api = inject(RegulationsService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);
  private readonly destroyRef = inject(DestroyRef);
  private readonly auth = inject(AuthService);
  private readonly personal = inject(PersonalService);
  private preferenceRequest?: Subscription;
  private catalogRequest?: Subscription;
  readonly speciesList = signal<Species[]>([]);
  readonly catalog = signal<Catalog | null>(null);
  readonly loading = signal(true);
  readonly error = signal('');
  readonly preferenceNotice = signal('');
  isModalOpen = false;
  searchQuery = '';
  selectedSpecies: Species | null = null;
  landType = '';
  huntingDate = this.localToday();
  zone = '';
  dmu = '';
  regulatoryArea = '';
  managedArea = '';
  landownerPermission = false;
  @ViewChild('speciesSearch') private speciesSearch?: ElementRef<HTMLInputElement>;
  @ViewChild('speciesButton') private speciesButton?: ElementRef<HTMLButtonElement>;

  constructor() {
    let ownerId = this.auth.currentUser()?.id;
    effect(() => {
      const nextOwnerId = this.auth.currentUser()?.id;
      if (ownerId === nextOwnerId) return;
      ownerId = nextOwnerId;
      this.preferenceRequest?.unsubscribe();
      this.preferenceNotice.set('');
      this.applySearchParameters();
      this.isModalOpen = false;
      this.searchQuery = '';
      if (nextOwnerId !== undefined && this.catalog()) this.loadPreferences(nextOwnerId);
    });
  }

  ngOnInit(): void {
    this.auth.ensureSession().pipe(takeUntilDestroyed(this.destroyRef)).subscribe();
    this.loadCatalog();
  }

  loadCatalog(): void {
    this.catalogRequest?.unsubscribe();
    this.preferenceRequest?.unsubscribe();
    this.loading.set(true);
    this.error.set('');
    this.preferenceNotice.set('');
    this.catalogRequest = forkJoin({ species: this.api.species(), catalog: this.api.catalog() })
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: ({ species, catalog }) => {
          this.speciesList.set(species);
          this.catalog.set(catalog);
          this.applySearchParameters();
          this.loading.set(false);
          const ownerId = this.auth.currentUser()?.id;
          if (ownerId !== undefined) this.loadPreferences(ownerId);
        },
        error: error => {
          this.loading.set(false);
          this.error.set(apiErrorMessage(error, 'Unable to load species and territories. Please try again.'));
        }
      });
  }

  private applySearchParameters(): void {
    const catalog = this.catalog();
    const params = this.route.snapshot.queryParamMap;
    this.selectedSpecies = this.speciesList().find(item => String(item.id) === params.get('species')) || null;
    const land = catalog?.land_types.find(item => String(item.id) === params.get('land_type'))
      || catalog?.land_types.find(item => item.is_private) || catalog?.land_types[0];
    this.landType = String(land?.id || '');
    this.huntingDate = params.get('date') || this.localToday();
    this.zone = params.get('zone') || ''; this.dmu = params.get('dmu') || '';
    this.regulatoryArea = params.get('regulatory_area') || ''; this.managedArea = params.get('managed_area') || '';
    this.landownerPermission = params.get('landowner_permission') === 'true';
  }

  private loadPreferences(ownerId: number): void {
    if (this.route.snapshot.queryParamMap.keys.length) return;
    this.preferenceRequest?.unsubscribe();
    this.preferenceRequest = this.personal.preferences().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: preferences => {
        if (this.auth.currentUser()?.id !== ownerId || this.selectedSpecies || this.zone || this.dmu || this.managedArea || this.regulatoryArea || this.landownerPermission) return;
        this.applyPreferences(preferences);
      },
      error: () => {
        if (this.auth.currentUser()?.id === ownerId) this.preferenceNotice.set('Saved preferences could not be loaded. You can still enter a search.');
      }
    });
  }

  private applyPreferences(preferences: Preferences): void {
    const catalog = this.catalog();
    if (!catalog) return;
    this.selectedSpecies = this.speciesList().find(item => preferences.species.includes(item.id)) || null;
    this.zone = String(catalog.zones.find(item => preferences.zones.includes(item.id))?.id || '');
    const area = catalog.managed_areas.find(item => preferences.managed_areas.includes(item.id));
    if (area) {
      const publicLand = catalog.land_types.find(item => !item.is_private &&
        (area.area_type === 'WMA' ? item.name.includes('WMA') : item.name.includes('Commission')))
        || catalog.land_types.find(item => !item.is_private);
      this.landType = String(publicLand?.id || this.landType);
      this.managedArea = String(area.id);
    }
    if (this.selectedSpecies || this.zone || area) this.preferenceNotice.set('Filled from your saved preferences. Adjust these selections for your trip.');
  }

  get filteredSpecies(): Species[] {
    const query = this.searchQuery.toLowerCase();
    return this.speciesList().filter(item => item.name.toLowerCase().includes(query) || item.scientific.toLowerCase().includes(query));
  }

  get selectedLandType() {
    return this.catalog()?.land_types.find(item => String(item.id) === this.landType);
  }

  get filteredDMUs() {
    return this.catalog()?.dmus.filter(item => !this.zone || String(item.zone_id) === this.zone) || [];
  }

  get supportedScopes() {
    return this.catalog()?.supported_scopes?.filter(scope =>
      (!this.selectedSpecies || scope.species === this.selectedSpecies.id) && String(scope.land_type) === this.landType) || [];
  }

  get filteredRegulatoryAreas() {
    return regulatoryAreasFor(this.catalog(), { species: String(this.selectedSpecies?.id || ''),
      land_type: this.landType, managed_area: this.managedArea });
  }

  scopeAreaNames(scope: NonNullable<Catalog['supported_scopes']>[number]): string {
    const ids = Array.isArray(scope.scopes.managed_area) ? scope.scopes.managed_area : [scope.scopes.managed_area];
    return this.catalog()?.managed_areas.filter(area => ids.includes(area.id)).map(area => area.name).join(', ') || '';
  }

  get unsupportedManagedArea(): boolean {
    if (!this.selectedSpecies || !this.managedArea || !this.selectedLandType?.requires_managed_area) return false;
    return !this.supportedScopes.some(scope => {
      const area = scope.scopes.managed_area;
      return area === undefined || (Array.isArray(area) ? area.includes(Number(this.managedArea)) : area === Number(this.managedArea));
    });
  }

  setLandType(id: number): void {
    this.landType = String(id);
    this.zone = '';
    this.dmu = '';
    this.regulatoryArea = '';
    this.managedArea = '';
    this.landownerPermission = false;
  }

  openModal(): void { this.isModalOpen = true; setTimeout(() => this.speciesSearch?.nativeElement.focus()); }
  closeModal(): void { this.isModalOpen = false; this.searchQuery = ''; this.speciesButton?.nativeElement.focus(); }
  selectSpecies(species: Species): void { this.selectedSpecies = species; this.regulatoryArea = ''; this.closeModal(); }

  selectorKeydown(event: KeyboardEvent): void {
    if (event.key === 'Escape') { this.closeModal(); event.preventDefault(); return; }
    if (event.key !== 'Tab') return;
    const panel = event.currentTarget as HTMLElement;
    const targets = Array.from(panel.querySelectorAll<HTMLElement>('button:not(:disabled), input:not(:disabled)'));
    const first = targets[0], last = targets[targets.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
    if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
  }

  checkRegulations(): void {
    if (!this.selectedSpecies || !this.landType || !this.huntingDate || this.loading()) return;
    if (this.selectedLandType?.requires_managed_area && !this.managedArea) {
      this.error.set('Select a public managed area before searching.');
      return;
    }
    const query: SearchQuery = {
      species: String(this.selectedSpecies.id), land_type: this.landType, date: this.huntingDate,
      zone: this.zone, dmu: this.dmu, regulatory_area: this.regulatoryArea, managed_area: this.managedArea,
      landowner_permission: String(this.landownerPermission)
    };
    this.error.set('');
    void this.router.navigate(['/results'], { queryParams: query });
  }

  private localToday(): string {
    const date = new Date();
    return [date.getFullYear(), String(date.getMonth() + 1).padStart(2, '0'), String(date.getDate()).padStart(2, '0')].join('-');
  }
}
