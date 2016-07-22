import {BibleData} from 'data';
import {inject} from 'aurelia-framework';

@inject(BibleData)
export class Division {
  heading = 'Welcome to Thread Bible!';

  constructor(bibledata) {
    console.log(bibledata.mytest);
  }
}
