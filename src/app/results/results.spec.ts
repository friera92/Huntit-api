import { provideHttpClient } from '@angular/common/http';
import { DATE_PIPE_DEFAULT_OPTIONS } from '@angular/common';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, convertToParamMap, provideRouter } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { vi } from 'vitest';
import { AuthService } from '../services/auth.service';
import { AdditionalRecords, RegulationResult, SourceReference } from '../services/regulations.service';
import { Results } from './results';

const result: RegulationResult = {
  name: 'Wild Hog', scientific: 'Sus scrofa', image: '/hog.png', about: 'Source description.',
  behavior: '', tactics: '', landType: 'Private Land', dates: 'Not recorded', bag: 'Not recorded',
  licenses: 'Not recorded', methods: 'Not recorded', alerts: [],
  sources: [{ title: 'Official source', url: 'https://myfwc.com/example', retrieved_at: '2026-10-12T00:00:00Z', last_verified_at: null }],
  verified: false, matched_seasons: [], query: {}, status: 'unverified'
};

describe('Results API integration', () => {
  let fixture: ComponentFixture<Results>;
  let component: Results;
  let http: HttpTestingController;
  let params: BehaviorSubject<ReturnType<typeof convertToParamMap>>;

  beforeEach(async () => {
    params = new BehaviorSubject(convertToParamMap({}));
    await TestBed.configureTestingModule({
      imports: [Results],
      providers: [
        provideRouter([]), provideHttpClient(), provideHttpClientTesting(),
        { provide: DATE_PIPE_DEFAULT_OPTIONS, useValue: { timezone: '-0400' } },
        { provide: ActivatedRoute, useValue: { queryParamMap: params.asObservable() } }
      ]
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
    fixture = TestBed.createComponent(Results);
    component = fixture.componentInstance;
    fixture.detectChanges();
    http.expectOne('/api/catalog/').flush({
      land_types: [{ id: 2, name: 'Private Land', is_private: true, requires_managed_area: false }, { id: 3, name: 'WMA', is_private: false, requires_managed_area: true }],
      zones: [{ id: 4, code: 'A', name: 'Zone A' }], dmus: [],
      managed_areas: [{ id: 1, name: 'Example WMA', area_type: 'WMA' }], regulatory_areas: []
    });
  });

  afterEach(() => http.verify());

  it('requires URL search parameters instead of fabricating a hog result', () => {
    expect(component.activeResult()).toBeNull();
    expect(component.error()).toContain('Choose a species');
    http.expectNone(request => request.url === '/api/regulations/search/');
  });

  it('shows the selected public area references without claiming an open season', () => {
    const catalog = component.catalog()!;
    component.catalog.set({ ...catalog, managed_areas: [{ id: 1, name: 'Example WMA', area_type: 'WMA',
      brochure_url: 'https://app.myfwc.com/area', map_url: 'https://myfwc.com/maps' }] });
    component.filters = { species: '7', land_type: '3', date: '2026-11-03', managed_area: '1' };
    component.activeResult.set({ ...result, status: 'needs_review' });
    fixture.detectChanges();
    const element: HTMLElement = fixture.nativeElement;
    expect(element.querySelector('a[href="https://app.myfwc.com/area"]')).toBeTruthy();
    expect(element.querySelector('a[href="https://myfwc.com/recreation/notices/"]')).toBeTruthy();
    expect(element.textContent).toContain('does not establish an open hunting season');
    expect(element.textContent).toContain('awaiting review and publication');
  });

  it('hides public-area access references for private-land results', () => {
    component.filters = { species: '7', land_type: '2', date: '2026-11-03', managed_area: '1' };
    component.activeResult.set(result);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).not.toContain('Area Maps and Access');
  });

  it('keeps Fisheating sides separate from private turkey regions', () => {
    const catalog = component.catalog()!;
    component.catalog.set({ ...catalog,
      regulatory_areas: [{ id: 9, code: 'FISHEATING_EAST_US27', name: 'Fisheating east' },
        { id: 10, code: 'NORTH_SR70', name: 'North of SR70' }],
      supported_scopes: [{ title: 'Python east', species: 7, land_type: 3,
        scopes: { managed_area: 1, regulatory_area: 9 },
        coverage: { start_date: '2026-07-01', end_date: '2027-06-30' }, reviewed: false },
        { title: 'Turkey spring', species: 8, land_type: 2, scopes: { regulatory_area: 10 },
          coverage: { start_date: '2027-02-01', end_date: '2027-06-30' }, reviewed: false }]
    });
    component.filters = { species: '7', land_type: '3', managed_area: '1', date: '2027-03-06' };
    expect(component.filteredRegulatoryAreas.map(area => area.id)).toEqual([9]);
    component.filters = { species: '8', land_type: '2', date: '2027-03-20' };
    expect(component.filteredRegulatoryAreas.map(area => area.id)).toEqual([10]);
  });

  it('loads a refreshable URL and shows provenance and verification status', () => {
    params.next(convertToParamMap({ species: '7', land_type: '2', date: '2026-11-03', zone: '4', landowner_permission: 'true' }));
    const request = http.expectOne(request => request.url === '/api/regulations/search/');
    expect(request.request.params.get('date')).toBe('2026-11-03');
    expect(request.request.params.get('zone')).toBe('4');
    expect(request.request.params.get('landowner_permission')).toBe('true');
    request.flush(result);
    fixture.detectChanges();
    const text = fixture.nativeElement.textContent;
    expect(text).toContain('Wild Hog');
    expect(text).toContain('not independently verified');
    expect(text).toContain('Official source');
    expect(text).toContain('Not independently verified');
    expect(component.searchParams()?.date).toBe('2026-11-03');
  });

  it('shows server validation errors and clears a previous result', () => {
    params.next(convertToParamMap({ species: '7', land_type: '2', date: '2026-11-03' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush(result);
    params.next(convertToParamMap({ species: '8', land_type: '2', date: '2026-11-03' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush({ zone: ['Choose a hunting zone.'] }, { status: 400, statusText: 'Bad Request' });
    fixture.detectChanges();
    expect(component.activeResult()).toBeNull();
    expect(fixture.nativeElement.textContent).toContain('Choose a hunting zone.');
    expect(fixture.nativeElement.textContent).not.toContain('Wild Hog');
  });

  it('explains that no matching data does not determine whether hunting is allowed', () => {
    params.next(convertToParamMap({ species: '7', land_type: '2', date: '2026-11-03' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush({ ...result, status: 'no_data', sources: [] });
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('No matching records');
    expect(fixture.nativeElement.textContent).toContain('does not establish');
  });

  it('clears the previous result and Back filters when required URL parameters are removed', () => {
    params.next(convertToParamMap({ species: '7', land_type: '2', date: '2026-11-03' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush(result);
    expect(component.searchParams()?.species).toBe('7');
    params.next(convertToParamMap({ species: '7' }));
    fixture.detectChanges();
    expect(component.activeResult()).toBeNull();
    expect(component.searchParams()).toBeNull();
    expect(fixture.nativeElement.querySelector('.back-link').getAttribute('href')).toBe('/');
    expect(fixture.nativeElement.textContent).toContain('Choose a species');
    http.expectNone(request => request.url === '/api/regulations/search/');
  });

  it('saves authenticated search inputs without caching a regulatory answer', () => {
    TestBed.inject(AuthService).ensureSession().subscribe();
    http.expectOne('/api/auth/me/').flush({ id: 1, username: 'tester', email: '', first_name: '', last_name: '', is_staff: false });
    params.next(convertToParamMap({ species: '7', land_type: '2', date: '2026-11-03', landowner_permission: 'true' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush(result);
    component.searchTitle = 'Weekend hog hunt';
    component.saveSearch();
    http.expectOne('/api/auth/csrf/').flush({});
    const save = http.expectOne('/api/personal/saved-searches/');
    expect(save.request.body).toEqual({
      title: 'Weekend hog hunt', species: 7, land_type: 2, hunting_date: '2026-11-03',
      zone: null, dmu: null, regulatory_area: null, managed_area: null, landowner_permission: true
    });
    save.flush({ id: 4, ...save.request.body });
    expect(component.saveMessage()).toContain('Reopen it from your profile');
    expect(component.saving()).toBe(false);
  });

  it('clears incompatible land inputs and navigates so switching land refreshes results', () => {
    params.next(convertToParamMap({ species: '7', land_type: '2', date: '2026-11-03', managed_area: '1', landowner_permission: 'true' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush(result);
    const navigate = vi.spyOn(component.router, 'navigate').mockResolvedValue(true);
    component.filters.land_type = '3';
    component.changeLandType();
    expect(navigate).toHaveBeenCalledWith(['/results'], { queryParams: { species: '7', land_type: '3', date: '2026-11-03' } });
    expect(component.filters.managed_area).toBeUndefined();
    expect(component.filters.landowner_permission).toBeUndefined();
  });

  it('distinguishes unpublished rules from a reviewed closed season', () => {
    expect(component.resultStatus({ ...result, status: 'needs_review' })).toContain('awaiting review');
    expect(component.resultStatus({ ...result, status: 'closed' })).toContain('No open season');
    expect(component.resultStatus({ ...result, status: 'reviewed' })).toContain('Published, reviewed');
  });

  it('shows all approved species background, habitat, behavior and hunting guidance', () => {
    params.next(convertToParamMap({ species: '7', land_type: '2', date: '2026-11-03' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush({
      ...result, species_information_reviewed: true, habitat: 'Verified habitat detail.',
      behavior: 'Verified behavior detail.', tactics: 'Verified hunting guidance.'
    });
    fixture.detectChanges();
    const text = fixture.nativeElement.textContent;
    expect(text).toContain('Reviewed species background'); expect(text).toContain('Source description.');
    expect(text).toContain('Verified habitat detail.'); expect(text).toContain('Verified behavior detail.');
    expect(text).toContain('Verified hunting guidance.'); expect(text).not.toContain('Unreviewed Background');
  });

  it('keeps unapproved hunting guidance hidden when a working species record has not been approved', () => {
    params.next(convertToParamMap({ species: '7', land_type: '2', date: '2026-11-03' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush({ ...result, tactics: 'Unpublished hunting guidance.' });
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).not.toContain('Unpublished hunting guidance.');
  });

  it('displays every matching verified project period, condition and source alongside the primary answer', () => {
    const source: SourceReference = {
      title: 'Recorded FWC reference', url: 'https://myfwc.com/hunting/',
      retrieved_at: '2025-06-10T12:00:00Z', last_verified_at: '2026-10-12T12:00:00Z',
      original_last_verified_at: '2025-06-11T12:00:00Z', organization: 'FWC',
      effective_date: '2025-07-01', notes: 'Original source annotation.', document_type: 'Regulation booklet',
      verification_basis: 'Project owner confirmed verification of the existing records.'
    };
    const additional: AdditionalRecords = {
      verified_at: '2026-10-12T12:00:00Z', verification_basis: source.verification_basis!,
      seasons: [{
        id: 1, name: 'Recorded archery season', code: 'ARCH', season_year: '2025–2026', scope: 'Private Land · Zone A', category: 'Archery',
        periods: [{ start_date: '2025-08-01', end_date: '2025-08-31', notes: 'First segment.' }, { start_date: '2025-09-01', end_date: '2025-09-15', notes: 'Second segment.' }],
        matches_date: false, year_round: false, bag: 'Recorded season bag.', licenses: 'Recorded permit.',
        methods: 'Recorded bow restriction.', notes: 'Original season condition.', source
      }],
      bag_rules: [{ id: 2, limit_type: 'DAILY', season_year: '2025–2026', scope: 'Private Land · Zone A', category: 'Archery', limit: 2, is_unlimited: false, conditions: 'Original daily condition.', source }],
      notes: [{ id: 3, title: 'Recorded regional restriction', text: 'Original advisory text.', season_year: '2025–2026', scope: 'Zone A', source }]
    };
    params.next(convertToParamMap({ species: '7', land_type: '2', date: '2026-11-03' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush({ ...result, additional_records: additional });
    fixture.detectChanges();
    const text = fixture.nativeElement.textContent;
    expect(text).toContain('Additional Verified Project Records');
    for (const fragment of ['2025-08-01 through 2025-08-31', 'First segment.', '2025-09-01 through 2025-09-15', 'Second segment.',
      'Season code: ARCH', 'selected date is outside', 'Recorded season bag.', 'Recorded permit.', 'Recorded bow restriction.',
      'Original season condition.', 'Daily limit', 'Limit: 2', 'Original daily condition.', 'Original advisory text.',
      'Organization: FWC', 'Document type: Regulation booklet', 'Source effective date: 2025-07-01', 'Original source verification date:', 'Original source annotation.', 'Verification confirmed by the project owner.']) {
      expect(text).toContain(fragment);
    }
    expect(fixture.nativeElement.querySelector('a[href="https://myfwc.com/hunting/"]').getAttribute('rel')).toBe('noopener noreferrer');
    expect(text).not.toContain(source.verification_basis!);
    expect(component.activeResult()?.additional_records?.verification_basis).toBe(source.verification_basis);
    expect(text).toContain('Not recorded'); // The primary answer remains visible as supplied.
  });

  it('distinguishes a zero bag limit from missing data and does not invent bounds for a year-round record', () => {
    const source = result.sources[0];
    params.next(convertToParamMap({ species: '7', land_type: '2', date: '2026-11-03' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush({
      ...result, additional_records: {
        verified_at: '2026-10-12T12:00:00Z', verification_basis: 'Project owner confirmation',
        seasons: [{ id: 1, name: 'Year-round record', code: '', season_year: '2025–2026', scope: 'Private Land', category: '', periods: [], matches_date: false, year_round: true, bag: '', licenses: '', methods: '', notes: '', source }],
        bag_rules: [
          { id: 2, limit_type: 'DAILY', season_year: '2025–2026', scope: 'Private Land', category: '', limit: 0, is_unlimited: false, conditions: '', source },
          { id: 3, limit_type: 'SEASON', season_year: '2025–2026', scope: 'Private Land', category: '', limit: null, is_unlimited: false, conditions: '', source: null }
        ], notes: []
      }
    });
    fixture.detectChanges();
    const text = fixture.nativeElement.textContent;
    expect(text).toContain('Limit: 0'); expect(text).toContain('Limit: Not recorded');
    expect(text).toContain('Source reference: Not recorded.');
    expect(text).toContain('Recorded as year-round for 2025–2026');
    expect(text).toContain('Explicit start and end dates were not supplied.');
  });

  it('shows scoped advisory text without treating it as an open season or executing record content', () => {
    params.next(convertToParamMap({ species: '7', land_type: '3', date: '2026-11-03', managed_area: '1' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush({
      ...result, status: 'no_data', additional_records: {
        verified_at: '2026-10-12T12:00:00Z', verification_basis: 'Project owner confirmation', seasons: [], bag_rules: [],
        notes: [{ id: 1, title: 'WMA advisory', text: '<img src=x onerror=alert(1)> Check this area’s seasons.', season_year: '2025–2026', scope: 'Example WMA advisory',
          source: { ...result.sources[0], title: 'Unsafe reference', url: 'javascript:alert(1)' } }]
      }
    });
    fixture.detectChanges();
    const text = fixture.nativeElement.textContent;
    expect(text).toContain('No matching records'); expect(text).toContain('does not establish');
    expect(text).toContain('Example WMA advisory'); expect(text).toContain('<img src=x onerror=alert(1)>');
    expect(fixture.nativeElement.querySelector('img[src="x"]')).toBeNull();
    expect(fixture.nativeElement.querySelector('a[href^="javascript:"]')).toBeNull();
    expect(text).not.toContain('Matches the selected date according to this record.');
  });

  it('keeps recorded UTC source and approval dates on their original day in a US timezone', () => {
    const source = {
      ...result.sources[0], retrieved_at: '2026-10-07T00:00:00Z',
      last_verified_at: '2026-10-07T00:00:00Z', original_last_verified_at: '2026-10-07T00:00:00Z'
    };
    params.next(convertToParamMap({ species: '7', land_type: '2', date: '2026-11-03' }));
    http.expectOne(request => request.url === '/api/regulations/search/').flush({
      ...result, species_information_reviewed: true, species_information_verified_at: '2026-10-07T00:00:00Z',
      sources: [source], additional_records: {
        verified_at: '2026-10-07T00:00:00Z', verification_basis: 'Project owner confirmation',
        seasons: [], bag_rules: [], notes: [{ id: 1, title: 'Original note', text: 'Original detail.', season_year: '2026', scope: 'Private Land', source }]
      }
    });
    fixture.detectChanges();
    const text: string = fixture.nativeElement.textContent;
    expect(text).toContain('Species information verified: Oct 7, 2026');
    expect(text).toContain('Verification confirmed: Oct 7, 2026');
    expect(text).toContain('Last verified: Oct 7, 2026');
    expect(text.match(/Retrieved: Oct 7, 2026/g)).toHaveLength(2);
    expect(text.match(/Original source verification date: Oct 7, 2026/g)).toHaveLength(2);
    expect(text).not.toContain('Oct 6, 2026');
  });
});
