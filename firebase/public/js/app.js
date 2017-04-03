var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!',
    book: [],
    bookName: 'Matthew',
    contents: [],
    curWord: undefined,
    curWordCount: 0,
    curWordBkCount: 0,
    menuVisible: false,
    curBookContents: {}
  },
  directives: {
    scroll: {
      bind: function(el, binding) {
        el.addEventListener('scroll',function(e){
          binding.value(e, { scrollTop: el.scrollTop, scrollLeft: el.scrollLeft});
        });

        var spans = el.querySelectorAll('span.chnum');
        console.log(spans);
        spans.forEach(function(span) {
          var rect = span.getBoundingClientRect();
          console.log(rect);
        });
      }
    }
  },

  methods: {
    selectWord: function(word) {
      console.log(word);
      console.log('pos: ' + word.s);
      console.log('text: ' + word.t);
      console.log('lemma: ' + word.l);
      console.log('heading: ' + word.h);
      console.log('whitespace: ' + word.w);
      this.curWord = word;
      console.log(word.l);
      var that = this;
      this.database.ref('/search/'+word.l).once('value').then(function(data) {
        var val = data.val();
        that.curWordCounts = val;
        that.curWordCount = val.count;
        that.curWordBkCount = that.getWordCount(that.bookName);
      });
    },

    getWordCount: function(bookName) {
      if (this.curWordCounts == undefined) {
        return 0;
      }
      var bk = this.curWordCounts.refs[bookName];
      if (bk == undefined) {
        return 0;
      }
      return bk.count;
    },

    isSameWord: function(word1, word2) {
      if (word1 == undefined || word2 == undefined) {
        return;
      }
      var sameWord = false;
      if (word1.l != undefined && word2.l != undefined && word1.l == word2.l) {
        sameWord = true;
      } else if (word1.l != undefined && word1.l == word2.t) {
        sameWord = true;
      } else if (word2.l != undefined && word1.t == word2.l) {
        sameWord = true;
      } else if (word1.t == word2.t) {
        sameWord = true;
      }
      return { sel: sameWord}
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
    this.database = database;
    database.ref('/chapters/en/net/').once('value').then(function(data) {
      console.log(data.val());
      that.contents = data.val();
      that.curBookContents = that.contents[5].books[0];
    });

    database.ref('/en/net/matthew/').once('value').then(function(data) {
      console.log(data.val());
      that.book = data.val();
    });

  }
})
