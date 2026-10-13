import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Results } from './results/results';
import { Log } from './log/log';
import { Licenses } from './licenses/licenses';
import { Profile } from './profile/profile';
import { Account } from './auth/account';
import { authGuard } from './auth/auth.guard';
import { AccountSettings } from './settings/account-settings';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'results', component: Results },
  { path: 'log', component: Log, canActivate: [authGuard] },
  { path: 'licenses', component: Licenses, canActivate: [authGuard] },
  { path: 'profile', component: Profile, canActivate: [authGuard] },
  { path: 'settings', component: AccountSettings, canActivate: [authGuard] },
  { path: 'login', component: Account, data: { register: false } },
  { path: 'register', component: Account, data: { register: true } },
  { path: '**', redirectTo: '' }
];
