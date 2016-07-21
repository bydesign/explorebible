import {BibleData} from 'data';
import {inject} from 'aurelia-framework';

@inject(BibleData)
export class Bible {
  heading = 'Welcome to Thread Bible!';

  constructor(bibledata) {
    var that = this;
    bibledata.books.then(response => response.json()).then(function(data) {
      that.divisions = data;
      console.log(data);
    });
  }

  attached() {
    console.log('attached to view');
    console.log(this.divisions);
  }
}
