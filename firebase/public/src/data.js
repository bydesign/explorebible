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

  get_cached_data(uri, propname) {
      var that = this;
      var p = {};
      if (that[propname] == undefined) {
        p = new Promise(function(resolve, reject) {
          that.http.fetch(uri).then(response => response.json()).then(function(data) {
            that[propname] = data;
            resolve(data);
          });
        });

      } else {
        p = new Promise(function(resolve, reject) {
          resolve(that[propname]);
        });
      }
      return p;
  }

  get books() {
    return this.get_cached_data('books/en.json', '_book').then(function(divs) {
      if (divs[0].books[0].c == undefined) {
        divs.forEach(function(div) {
          div.books.forEach(function(book) {
            book.c = [];
            for (var i=0, len=book.ct; i<len; i++) {
              book.c.push({ c:{ length:50 } });
            }
          });
        });
      }
      return divs;
    });
  }
}
