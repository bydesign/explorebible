var app = angular.module("exploreBible", ["firebase"]);
app.controller("BibleCtrl", function($scope, $firebaseArray, $http) {
  var ref = firebase.database().ref().child("messages");
  var sentRef = firebase.database().ref().child("sentences");
  $scope.sents = $firebaseArray(sentRef);
  var booksRef = firebase.database().ref().child("books/en");
  $scope.bible = $firebaseArray(booksRef);
  console.log($scope.bible);

  $scope.getTimes=function(n){
     return new Array(n);
  };

  $scope.selectWord = function(word, sent) {
    $scope.selectedWord = word;
    $scope.selectedSent = sent;
  };

  $scope.calcOccur = function(selectedWord) {
    if (selectedWord != undefined) {
      var count = 0;
      angular.forEach($scope.sents, function(sent) {
        angular.forEach(sent.words, function(word) {
          if (word.lemma == selectedWord.lemma) {
            count++;
          }
        });
      });
      return count;
    }
  }

});
