import { Component, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterOutlet } from '@angular/router';

@Component({
  selector: 'upload-form',
  templateUrl: './upload-form.html',
  styleUrl: './upload-form.css',
})
export class UploadForm {
  file?: File;
  id = signal(0);
  imageSuffix = signal('');
  imageSrc = computed(() => {
    const suffix = this.imageSuffix() ? `?${this.imageSuffix()}` : '';
    return `/api/inventory/static/${this.id()}` + suffix;
  });
  activatedRoute = inject(ActivatedRoute);

  constructor() {
    this.activatedRoute.params.subscribe((params) => {
      this.id.set(Number(params['id']));
    });
  }

  onFileChange(event: Event) {
    const fileInput = event.target as HTMLInputElement;
    this.file = fileInput.files?.[0];
  }

  async upload(event: Event) {
    event.preventDefault();

    if (!this.file) {
      return;
    }

    const data = new FormData();
    data.append('file', this.file);

    const resp = await fetch(`/api/inventory/${this.id()}`, {
      method: 'POST',
      body: data,
    });
    await resp.text();

    this.imageSuffix.set(String(Math.random()));
  }
}
