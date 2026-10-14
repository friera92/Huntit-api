import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { catchError, EMPTY, filter, Observable, of, switchMap, throwError } from 'rxjs';
import { SearchQuery } from './regulations.service';
import { AuthService } from './auth.service';

export interface Preferences {
  species: number[];
  managed_areas: number[];
  zones: number[];
}
export interface LicenseInput {
  permit: number | null;
  name: string;
  status: 'unknown' | 'held' | 'not_held' | 'expired';
  valid_from: string | null;
  expires_on: string | null;
  notes: string;
}
export interface UserLicense extends LicenseInput { id: number; }
export interface HarvestInput {
  species: number;
  harvest_date: string;
  managed_area: number | null;
  location: string;
  quantity: number;
  notes: string;
}
export interface Harvest extends HarvestInput {
  id: number;
  species_name: string;
  species_image: string;
  managed_area_name: string | null;
  archived_at: string | null;
}
export interface SavedSearchInput {
  title: string;
  species: number;
  land_type: number;
  hunting_date: string;
  zone: number | null;
  dmu: number | null;
  regulatory_area: number | null;
  managed_area: number | null;
  landowner_permission: boolean;
}
export interface SavedSearch extends SavedSearchInput { id: number; }
export interface ResetOptions {
  preferences: boolean; saved_searches: boolean; licenses: boolean;
  harvests: 'archive' | 'keep'; confirmation: string;
}

/** Store search inputs only: reopening requests the current regulation records. */
export function savedSearchQuery(search: SavedSearch): SearchQuery {
  const query: SearchQuery = {
    species: String(search.species), land_type: String(search.land_type), date: search.hunting_date,
    landowner_permission: String(search.landowner_permission)
  };
  for (const key of ['zone', 'dmu', 'regulatory_area', 'managed_area'] as const) {
    if (search[key] !== null) query[key] = String(search[key]);
  }
  return query;
}

@Injectable({ providedIn: 'root' })
export class PersonalService {
  private readonly http = inject(HttpClient);
  private readonly auth = inject(AuthService);
  private readonly base = '/api/personal/';

  preferences(): Observable<Preferences> { return this.forOwner(this.http.get<Preferences>(`${this.base}preferences/`)); }
  savePreferences(value: Preferences): Observable<Preferences> {
    return this.mutate(() => this.http.put<Preferences>(`${this.base}preferences/`, value));
  }
  licenses(): Observable<UserLicense[]> { return this.forOwner(this.http.get<UserLicense[]>(`${this.base}licenses/`)); }
  saveLicense(value: LicenseInput, id?: number): Observable<UserLicense> {
    return this.mutate(() => id === undefined
      ? this.http.post<UserLicense>(`${this.base}licenses/`, value)
      : this.http.patch<UserLicense>(`${this.base}licenses/${id}/`, value));
  }
  deleteLicense(id: number): Observable<void> {
    return this.mutate(() => this.http.delete<void>(`${this.base}licenses/${id}/`));
  }
  harvests(archived = false): Observable<Harvest[]> {
    return this.forOwner(this.http.get<Harvest[]>(`${this.base}harvests/`, archived ? { params: { archived: 'true' } } : {}));
  }
  saveHarvest(value: HarvestInput, id?: number): Observable<Harvest> {
    return this.mutate(() => id === undefined
      ? this.http.post<Harvest>(`${this.base}harvests/`, value)
      : this.http.patch<Harvest>(`${this.base}harvests/${id}/`, value));
  }
  deleteHarvest(id: number): Observable<void> {
    return this.mutate(() => this.http.delete<void>(`${this.base}harvests/${id}/`));
  }
  archiveHarvest(id: number): Observable<Harvest> {
    return this.mutate(() => this.http.post<Harvest>(`${this.base}harvests/${id}/archive/`, {}));
  }
  restoreHarvest(id: number): Observable<Harvest> {
    return this.mutate(() => this.http.post<Harvest>(`${this.base}harvests/${id}/restore/`, {}));
  }
  savedSearches(): Observable<SavedSearch[]> { return this.forOwner(this.http.get<SavedSearch[]>(`${this.base}saved-searches/`)); }
  saveSearch(value: SavedSearchInput): Observable<SavedSearch> {
    return this.mutate(() => this.http.post<SavedSearch>(`${this.base}saved-searches/`, value));
  }
  renameSearch(id: number, title: string): Observable<SavedSearch> {
    return this.mutate(() => this.http.patch<SavedSearch>(`${this.base}saved-searches/${id}/`, { title }));
  }
  deleteSearch(id: number): Observable<void> {
    return this.mutate(() => this.http.delete<void>(`${this.base}saved-searches/${id}/`));
  }
  exportData(): Observable<Blob> {
    return this.forOwner(this.http.get(`${this.base}export/`, { responseType: 'blob' }));
  }
  resetData(options: ResetOptions): Observable<unknown> {
    return this.mutate(() => this.http.post(`${this.base}reset/`, options));
  }
  private mutate<T>(request: () => Observable<T>): Observable<T> {
    const ownerId = this.auth.currentUser()?.id;
    // A newly loaded session may not have a CSRF cookie yet. Angular sends it as X-CSRFToken.
    return this.forOwner(this.http.get('/api/auth/csrf/').pipe(
      switchMap(() => ownerId === this.auth.currentUser()?.id ? request() : EMPTY)
    ), ownerId);
  }
  private forOwner<T>(request: Observable<T>, ownerId = this.auth.currentUser()?.id): Observable<T> {
    return request.pipe(
      filter(() => ownerId === this.auth.currentUser()?.id),
      catchError(error => {
        if (ownerId !== this.auth.currentUser()?.id) return EMPTY;
        if (error instanceof HttpErrorResponse && [401, 403].includes(error.status)) {
          // A denied request can mean an expired session or a CSRF error. Confirm identity
          // before clearing private screens; a valid session must survive a CSRF failure.
          return this.auth.refreshSession().pipe(
            catchError(() => of(null)), switchMap(() => throwError(() => error))
          );
        }
        return throwError(() => error);
      })
    );
  }
}
