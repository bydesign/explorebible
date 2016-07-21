export class App {
  configureRouter(config, router) {
    config.title = 'ThreadBible';
    config.map([
      { route: ['','bible'], name: 'bible', moduleId: './bible', nav: true, title:'Bible' },
      { route: ['div'], name: 'division', moduleId: './division', nav: true, title:'Division' },
      { route: ['book'], name: 'book', moduleId: './book', nav: true, title:'Book' },
      { route: ['chap'], name: 'chapter', moduleId: './chapter', nav: true, title:'Chapter' },
      { route: ['verse'], name: 'verse', moduleId: './verse', nav: true, title:'Verse' }
    ]);

    this.router = router;
  }
}
