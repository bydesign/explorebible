var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!',
    book: [],
    bookName: 'Matthew',
    contents: [],
    curWord: undefined,
    menuVisible: false,
    curBookContents: {}
  },
  directives: {
    scroll: {
      bind: function(el, binding) {
        el.addEventListener('scroll',function(e){
          binding.value(e, { scrollTop: el.scrollTop, scrollLeft: el.scrollLeft});
        });
      }
    }
  },

  methods: {
    selectWord: function(word) {
      console.log(word);
      console.log(word.s);
      console.log(word.t);
      console.log(word.l);
      console.log(word.h);
      console.log(word.w);
      this.curWord = word;
    },

    verseWidth: function(wordCount) {
      if (this.isInteger(wordCount)) {
        var length = (wordCount - 2) / 40;
        if (length > 1) {
          length = 1;
        }
        return {
          width: 60 + length * 40 + '%'
        };
      } else {
        return {};
      }
    },

    isInteger: function(val) {
      return (typeof val==='number' && (val%1)===0);
    },

    onScroll:function(e, position){
      this.position = position;
      console.log(position);
    }
  },

  created: function () {
    var that = this;
    // Set the configuration for your app
    // TODO: Replace with your project's config object
    var config = {
      apiKey: "AIzaSyC3gNu-QFNgVCWU8zMvkurXNNgMY2tDjhE",
      authDomain: "project-6084703088352496772.firebaseapp.com",
      databaseURL: "https://project-6084703088352496772.firebaseio.com",
      storageBucket: "project-6084703088352496772.appspot.com"
    };
    firebase.initializeApp(config);

    // Get a reference to the database service
    var database = firebase.database();
    database.ref('/chapters/en/net/').once('value').then(function(data) {
      console.log(data.val());
      that.contents = data.val();
      that.curBookContents = that.contents[5].books[0];
    });

    database.ref('/en/net/matthew/').once('value').then(function(data) {
      console.log(data.val());
      that.book = data.val();
    });

    var el = document.querySelector('zoomChap span');
    console.log(el);
    var rect = el.getBoundingClientRect();
    console.log(rect);

  }
})
