var app = angular.module("exploreBible", ["firebase"]);
app.controller("BibleCtrl", function($scope, $firebaseArray, $http) {
  var ref = firebase.database().ref().child("messages");
  var sentRef = firebase.database().ref().child("sentences");
  $scope.sents = $firebaseArray(sentRef);
  var booksRef = firebase.database().ref().child("books");
  $scope.divisions = $firebaseArray(booksRef);
  /*$http({
      method : "GET",
      url : "/data/verse_data.json"
  }).then(function mySuccess(response) {
      angular.forEach(response.data, function(item) {
        $scope.sents.$add(item);
        console.log(item);
      });

  }, function myError(response) {
      console.log(response.statusText);
  });*/

  /*$http({
      method : "GET",
      url : "/data/books.json"
  }).then(function mySuccess(response) {
      angular.forEach(response.data, function(item) {
        $scope.books.$add(item);
        console.log(item);
      });

  }, function myError(response) {
      console.log(response.statusText);
  });*/

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

  // create a synchronized array
  $scope.messages = $firebaseArray(ref);
  // add new items to the array
  // the message is automatically added to our Firebase database!
  $scope.addMessage = function() {
    $scope.messages.$add({
      text: $scope.newMessageText
    });
  };
  // click on `index.html` above to see $remove() and $save() in action
});
