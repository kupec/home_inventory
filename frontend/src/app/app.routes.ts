import { Routes } from '@angular/router';
import { UploadForm } from '../upload/upload-form';

export const routes: Routes = [
  {path: 'inventory/:id', component: UploadForm}
];
