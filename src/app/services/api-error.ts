import { HttpErrorResponse } from '@angular/common/http';

export function apiErrorMessage(error: unknown, fallback: string): string {
  if (!(error instanceof HttpErrorResponse)) return fallback;
  if (error.status === 0) return 'Cannot reach the local server. Check that the Django server is running.';
  if (error.status >= 500 || !error.error || typeof error.error !== 'object') return fallback;
  const messages: string[] = [];
  for (const value of Object.values(error.error)) {
    for (const item of Array.isArray(value) ? value : [value]) {
      if (typeof item === 'string') messages.push(item.replace(/<[^>]*>/g, '').replace(/[\u0000-\u001f]/g, ' '));
    }
  }
  return messages.join(' ').slice(0, 600) || fallback;
}
