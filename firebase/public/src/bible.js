import {BibleData} from 'data';
import {inject} from 'aurelia-framework';

@inject(BibleData)
export class Bible {
  heading = 'Welcome to Thread Bible!';

  constructor(bibledata) {
    var that = this;
    bibledata.books.then(function(data) {
      that.divisions = data;
    });
  }

  attached() {
    //console.log('attached to view');
    //console.log(this.divisions);
  }
}
