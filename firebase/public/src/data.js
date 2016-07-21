import {HttpClient} from 'aurelia-fetch-client';
import {inject} from 'aurelia-framework';
import 'fetch';

@inject(HttpClient)
export class BibleData {
  constructor(http) {
    http.configure(config => {
      config
        .useStandardConfiguration()
        .withBaseUrl('https://project-6084703088352496772.firebaseio.com/');
    });
    this.http = http;
  }

  get books() {
    return this.http.fetch('books/en.json');
  }
}
