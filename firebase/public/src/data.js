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
    var that = this;
    var p = {};
    if (this._books == undefined) {
      p = new Promise(function(resolve, reject) {
        that.http.fetch('books/en.json').then(response => response.json()).then(function(data) {
          that._books = data;
          resolve(data);
        });
      });

    } else {
      p = new Promise(function(resolve, reject) {
        resolve(that._books);
      });
    }

    return p;
  }
}
