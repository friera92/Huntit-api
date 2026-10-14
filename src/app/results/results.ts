import { Component, DestroyRef, effect, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { catchError, finalize, of, Subject, switchMap, takeUntil, tap } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { AdditionalRecords, Catalog, regulatoryAreasFor, RegulationResult, RegulationsService, SearchQuery } from '../services/regulations.service';
import { apiErrorMessage } from '../services/api-error';
import { AuthService } from '../services/auth.service';
import { PersonalService, SavedSearchInput } from '../services/personal.service';

@Component({
  selector: 'app-results',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './results.html',
  styleUrls: ['./results.css', '../personal-forms.css']
})
export class Results implements OnInit {
  private readonly api = inject(RegulationsService);
  private readonly route = inject(ActivatedRoute);
  readonly router = inject(Router);
  private readonly personal = inject(PersonalService);
  readonly user = inject(AuthService).currentUser;
  private readonly destroyRef = inject(DestroyRef);
  private readonly ownerChanged = new Subject<void>();
  readonly activeResult = signal<RegulationResult | null>(null);
  readonly loading = signal(false);
  readonly error = signal('');
  readonly searchParams = signal<SearchQuery | null>(null);
  readonly catalog = signal<Catalog | null>(null);
  readonly catalogError = signal('');
  readonly saving = signal(false);
  readonly saveError = signal('');
  readonly saveMessage = signal('');
  searchTitle = '';
  filters: SearchQuery = { species: '', land_type: '', date: '' };

  constructor() {
    let ownerId = this.user()?.id;
    effect(() => {
      const nextOwnerId = this.user()?.id;
      if (ownerId === nextOwnerId) return;
      ownerId = nextOwnerId;
      this.ownerChanged.next();
      this.saveMessage.set('');
      this.saveError.set('');
    });
  }

  get selectedLandType() { return this.catalog()?.land_types.find(item => String(item.id) === this.filters.land_type); }
  get selectedManagedArea() { return this.catalog()?.managed_areas.find(item => String(item.id) === this.filters.managed_area); }
  get filteredRegulatoryAreas() { return regulatoryAreasFor(this.catalog(), this.filters); }
  get filteredDMUs() { return this.catalog()?.dmus.filter(item => String(item.zone_id) === this.filters.zone) || []; }

  ngOnInit(): void {
    this.loadCatalog();
    this.route.queryParamMap.pipe(
      switchMap(params => {
        this.activeResult.set(null);
        this.searchParams.set(null);
        this.error.set('');
        this.saveError.set('');
        this.saveMessage.set('');
        const species = params.get('species');
        const landType = params.get('land_type');
        const date = params.get('date');
        if (!species || !landType || !date) {
          this.loading.set(false);
          this.error.set('Choose a species, land classification and hunting date to view regulations.');
          return of(null);
        }
        const query: SearchQuery = { species, land_type: landType, date };
        for (const key of ['zone', 'dmu', 'regulatory_area', 'managed_area', 'landowner_permission'] as const) {
          const value = params.get(key);
          if (value) query[key] = value;
        }
        this.searchParams.set(query);
        this.filters = { ...query };
        this.loading.set(true);
        return this.api.search(query).pipe(
          tap(() => this.loading.set(false)),
          catchError(error => {
            this.loading.set(false);
            this.error.set(apiErrorMessage(error, 'Unable to load regulations. Return to search and try again.'));
            return of(null);
          })
        );
      }),
      takeUntilDestroyed(this.destroyRef)
    ).subscribe(result => {
      this.activeResult.set(result);
      this.searchTitle = result ? `${result.name} · ${this.searchParams()?.date}`.slice(0, 120) : '';
    });
  }

  loadCatalog(): void {
    this.catalogError.set('');
    this.api.catalog().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: catalog => this.catalog.set(catalog),
      error: error => this.catalogError.set(apiErrorMessage(error, 'Unable to load search options. Please try again.'))
    });
  }

  changeLandType(): void {
    delete this.filters.managed_area;
    delete this.filters.landowner_permission;
    delete this.filters.zone;
    delete this.filters.dmu;
    delete this.filters.regulatory_area;
    this.updateFilters();
  }

  changeZone(): void { delete this.filters.dmu; this.updateFilters(); }
  changeArea(): void { delete this.filters.regulatory_area; this.updateFilters(); }

  updateFilters(): void { void this.router.navigate(['/results'], { queryParams: { ...this.filters } }); }

  saveSearch(): void {
    const query = this.searchParams();
    if (!query || !this.user() || this.saving() || !this.searchTitle.trim()) return;
    const value: SavedSearchInput = {
      title: this.searchTitle.trim(), species: Number(query.species), land_type: Number(query.land_type), hunting_date: query.date,
      zone: query.zone ? Number(query.zone) : null, dmu: query.dmu ? Number(query.dmu) : null,
      regulatory_area: query.regulatory_area ? Number(query.regulatory_area) : null,
      managed_area: query.managed_area ? Number(query.managed_area) : null,
      landowner_permission: query.landowner_permission === 'true'
    };
    this.saving.set(true);
    this.saveError.set('');
    this.saveMessage.set('');
    this.personal.saveSearch(value).pipe(
      finalize(() => this.saving.set(false)), takeUntil(this.ownerChanged), takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: () => {
        if (this.searchParams() === query) this.saveMessage.set('Search inputs saved. Reopen it from your profile to check current records.');
      },
      error: error => {
        if (this.searchParams() === query) this.saveError.set(apiErrorMessage(error, 'Unable to save this search. Please try again.'));
      }
    });
  }

  sourceUrl(url: string): string | null {
    return /^https?:\/\//i.test(url) ? url : null;
  }

  additionalRecordCount(records: AdditionalRecords): number {
    return records.seasons.length + records.bag_rules.length + records.notes.length;
  }

  limitTypeLabel(type: string): string {
    return ({ GENERAL: 'General limit', DAILY: 'Daily limit', POSSESSION: 'Possession limit', SEASON: 'Season limit', ANNUAL: 'Annual limit' } as Record<string, string>)[type] || type;
  }

  resultStatus(result: RegulationResult): string {
    switch (result.status) {
      case 'reviewed': return 'Published, reviewed records for these filters. Read the conditions and official sources before hunting.';
      case 'closed': return 'No open season for this date within the reviewed coverage. Do not treat another date or area as equivalent.';
      case 'needs_review': return 'Matching records are awaiting review and publication. No hunting authorization is established.';
      case 'no_data': return 'No matching records for these filters. This does not establish that hunting is permitted or prohibited.';
      default: return 'Imported source records — not independently verified. Confirm the official rules before hunting.';
    }
  }
}
