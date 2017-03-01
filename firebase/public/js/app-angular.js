var app = angular.module("exploreBible", ["firebase", 'ngSanitize']);

/*app.filter('trust', ['$sce', function($sce){
    return function(text) {
        return $sce.trustAsHtml(text);
    };
}]);*/

app.controller("BibleCtrl", function($scope, $firebaseArray, $http) {
  var ref = firebase.database().ref().child("messages");
  var sentRef = firebase.database().ref().child("sentences");
  $scope.sents = $firebaseArray(sentRef);
  //var booksRef = firebase.database().ref().child("books/en");
  var booksRef = firebase.database().ref().child("chapters/en/net");
  $scope.bible = $firebaseArray(booksRef);
  console.log($scope.bible);

  /*for (var i=1; i<=28; i++) {
    var mattRef = firebase.database().ref().child("en/net/matthew/"+i);
    $scope.matt = $firebaseArray(mattRef);
    console.log(i);
    console.log($scope.matt);
  }*/

  $scope.getArray=function(n){
     return new Array(n);
  };

  $scope.isStr = function(val) {
    return typeof(val) == 'string';
  };

  $scope.selectWord = function(word, sent) {
    $scope.selectedWord = word;
    $scope.selectedSent = sent;
  };

  $scope.selectDivision = function(div) {
    $scope.curDiv = div;
    $scope.view = 1;
    console.log('division selected: ' + div.name);
  };

  $scope.selectBook = function(book, div) {
    //console.log(book);
    //console.log(div);
    console.log('book selected: ' + book.name);
    var bookRef = firebase.database().ref().child("en/net/matthew");
    $scope.chapters = $firebaseArray(bookRef, function() { console.log('data loaded'); });
    console.log($scope.chapters);
    $scope.curDiv = div;
    $scope.view = 2;
    console.log('selectBook complete');
  };

  $scope.selectChapter = function(ch, book, div) {
    var chRef = firebase.database().ref().child("en/net/matthew/1/verse");
    $scope.curVerses = $firebaseArray(chRef);
    $scope.chapName = book.name + ' ' + ch.num;
    $scope.curBook = book;
    $scope.curDiv = div;
    $scope.view = 3;
  };

  $scope.calcOccur = function(selectedWord) {
    if (selectedWord != undefined) {
      var count = 0;
      angular.forEach($scope.curVerses, function(verse) {
        angular.forEach(verse.tokens, function(word) {
          if (word.text == selectedWord.text) {
            count++;
          }
        });
      });
      return count;
    }
  }

});
