import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Species {
  id: number;
  name: string;
  scientific: string;
  image: string;
  about: string;
  habitat?: string;
  behavior: string;
  tactics: string;
  species_information_reviewed?: boolean;
  species_information_verified_at?: string;
}
export interface SourceReference {
  title: string;
  url: string;
  retrieved_at: string | null;
  last_verified_at: string | null;
  source_checked_on?: string | null;
  evidence?: string;
  verification_basis?: string;
  original_last_verified_at?: string | null;
  effective_date?: string | null;
  organization?: string;
  document_type?: string;
  notes?: string;
}
export interface AdditionalSeason {
  id: number; name: string; code: string; season_year: string; scope: string; category: string;
  periods: { start_date: string; end_date: string; notes: string }[];
  matches_date: boolean; year_round: boolean;
  bag: string; licenses: string; methods: string; notes: string; source: SourceReference | null;
}
export interface AdditionalBagRule {
  id: number; limit_type: string; season_year: string; scope: string; category: string;
  limit: number | null; is_unlimited: boolean; conditions: string; source: SourceReference | null;
}
export interface AdditionalNote {
  id: number; title: string; text: string; season_year: string; scope: string; source: SourceReference | null;
}
export interface AdditionalRecords {
  verified_at: string;
  verification_basis: string;
  seasons: AdditionalSeason[];
  bag_rules: AdditionalBagRule[];
  notes: AdditionalNote[];
}
export interface Catalog {
  land_types: { id: number; name: string; is_private: boolean; requires_managed_area: boolean }[];
  zones: { id: number; code: string; name: string }[];
  dmus: { id: number; code: string; zone_id: number }[];
  regulatory_areas: { id: number; code: string; name: string }[];
  managed_areas: { id: number; name: string; area_type: string; brochure_url?: string;
    map_url?: string; county?: string; region?: string; description?: string }[];
  license_permits?: { id: number; name: string }[];
  supported_scopes?: {
    title: string; species: number; land_type: number;
    scopes: { zone?: number; dmu?: number; managed_area?: number | number[]; regulatory_area?: number };
    coverage: { start_date: string; end_date: string }; reviewed: boolean;
  }[];
}
export interface SearchQuery {
  species: string;
  land_type: string;
  date: string;
  zone?: string;
  dmu?: string;
  regulatory_area?: string;
  managed_area?: string;
  landowner_permission?: string;
}

export function regulatoryAreasFor(catalog: Catalog | null, query: Partial<SearchQuery>): Catalog['regulatory_areas'] {
  if (!catalog) return [];
  if (!catalog.supported_scopes) return catalog.regulatory_areas;
  const ids = new Set(catalog.supported_scopes.filter(scope => {
    if (String(scope.species) !== query.species || String(scope.land_type) !== query.land_type) return false;
    const area = scope.scopes.managed_area;
    return area === undefined || (Array.isArray(area) ? area : [area]).some(id => String(id) === query.managed_area);
  }).map(scope => scope.scopes.regulatory_area));
  return catalog.regulatory_areas.filter(area => ids.has(area.id));
}
export interface RegulationResult extends Omit<Species, 'id'> {
  landType: string;
  dates: string;
  bag: string;
  licenses: string;
  methods: string;
  alerts: string[];
  sources: SourceReference[];
  verified: boolean;
  matched_seasons: unknown[];
  query: Record<string, unknown>;
  status: 'unverified' | 'no_data' | 'reviewed' | 'closed' | 'needs_review';
  eligibility?: 'conditional' | 'permission_required' | 'no_open_season';
  coverage?: { start_date: string; end_date: string }[];
  additional_records?: AdditionalRecords;
}

@Injectable({ providedIn: 'root' })
export class RegulationsService {
  private readonly http = inject(HttpClient);
  species(): Observable<Species[]> {
    return this.http.get<Species[]>('/api/species/');
  }
  catalog(): Observable<Catalog> {
    return this.http.get<Catalog>('/api/catalog/');
  }
  search(query: SearchQuery): Observable<RegulationResult> {
    let params = new HttpParams();
    for (const [key, value] of Object.entries(query)) {
      if (value !== undefined && value !== '') params = params.set(key, value);
    }
    return this.http.get<RegulationResult>('/api/regulations/search/', { params });
  }
}
