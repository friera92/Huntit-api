import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Harvest } from '../services/personal.service';
import { Log } from './log';

const harvest: Harvest = { id: 9, species: 1, species_name: 'Wild Hog', species_image: '/hog.png', harvest_date: '2026-09-01', managed_area: null, managed_area_name: null, location: 'Private lease', quantity: 1, notes: 'Morning', archived_at: null };

describe('Private persisted harvest log', () => {
  let fixture: ComponentFixture<Log>;
  let http: HttpTestingController;
  function flushCatalog() {
    http.expectOne('/api/catalog/').flush({ land_types: [], zones: [], dmus: [], managed_areas: [], regulatory_areas: [] });
    http.expectOne('/api/species/').flush([{ id: 1, name: 'Wild Hog' }]);
  }
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Log], providers: [provideHttpClient(), provideHttpClientTesting()]
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
    fixture = TestBed.createComponent(Log);
    fixture.detectChanges();
    http.expectOne('/api/personal/harvests/').flush([harvest]);
    flushCatalog();
    fixture.detectChanges();
    await fixture.whenStable();
  });
  afterEach(() => http.verify());

  it('shows only loaded account records and removes the temporary photo preview workflow', () => {
    expect(fixture.nativeElement.textContent).toContain('Wild Hog');
    expect(fixture.nativeElement.textContent).not.toContain('Prototype');
    expect(fixture.nativeElement.querySelector('input[type=file]')).toBeNull();
  });

  it('creates a harvest then supports editing its persisted quantity and notes', () => {
    const component = fixture.componentInstance;
    component.form = { species: 1, harvest_date: '2026-09-02', location: 'Lease', managed_area: null, quantity: 2, notes: 'Second trip' };
    component.saveHarvest();
    http.expectOne('/api/auth/csrf/').flush({});
    const creation = http.expectOne('/api/personal/harvests/');
    expect(creation.request.body.species).toBe(1);
    creation.flush({ ...harvest, id: 10, quantity: 2 });
    expect(component.recentHarvests()).toHaveLength(2);
    component.editHarvest(harvest);
    component.form.quantity = 3;
    component.saveHarvest();
    http.expectOne('/api/auth/csrf/').flush({});
    const patch = http.expectOne('/api/personal/harvests/9/');
    expect(patch.request.method).toBe('PATCH');
    patch.flush({ ...harvest, quantity: 3 });
    expect(component.recentHarvests().find(item => item.id === 9)?.quantity).toBe(3);
  });

  it('archives an active harvest and reloads archived records for restoration', () => {
    const component = fixture.componentInstance;
    component.archiveHarvest(harvest);
    http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/personal/harvests/9/archive/').flush({ ...harvest, archived_at: '2026-10-12T00:00:00Z' });
    expect(component.recentHarvests()).toEqual([]);
    component.toggleArchive();
    const list = http.expectOne(request => request.url === '/api/personal/harvests/');
    expect(list.request.params.get('archived')).toBe('true');
    list.flush([{ ...harvest, archived_at: '2026-10-12T00:00:00Z' }]);
    flushCatalog();
    component.archiveHarvest(component.recentHarvests()[0], true);
    http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/personal/harvests/9/restore/').flush(harvest);
    expect(component.recentHarvests()).toEqual([]);
    expect(component.message()).toContain('restored');
  });

  it('requires explicit confirmation before permanent deletion and preserves records on failure', () => {
    const component = fixture.componentInstance;
    component.deleteHarvest(harvest);
    http.expectNone('/api/auth/csrf/');
    component.confirmingDelete = harvest.id;
    component.deleteHarvest(harvest);
    http.expectOne('/api/auth/csrf/').flush({});
    http.expectOne('/api/personal/harvests/9/').flush({ detail: 'Try again.' }, { status: 500, statusText: 'Error' });
    expect(component.recentHarvests()).toEqual([harvest]);
    expect(component.busy()).toBe(false);
  });
});
