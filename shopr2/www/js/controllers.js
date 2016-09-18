angular.module('starter.controllers', [])

.controller('DashCtrl', function($scope) {
  $scope.cards = [
    {  },
    {  }
  ];

  $scope.cardDestroyed = function(index) {
    $scope.cards.splice(index, 1);
  };

  $scope.cardSwiped = function(index) {
    var newCard = // new card data
    $scope.cards.push(newCard);
  };

})

.controller('ChatsCtrl', function($scope, Chats) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});


  $scope.chats = Chats.all();
  $scope.remove = function(chat) {
    Chats.remove(chat);
  };
})


.controller('CardsCtrl', function($scope, TDCardDelegate, $timeout, $http) {

  $scope.products = [];

  var cardTypes = [
    { image: 'http://c4.staticflickr.com/4/3924/18886530069_840bc7d2a5_n.jpg' },
    { image: 'http://c1.staticflickr.com/1/421/19046467146_548ed09e19_n.jpg' },
    { image: 'http://c1.staticflickr.com/1/278/18452005203_a3bd2d7938_n.jpg' },
    { image: 'http://c1.staticflickr.com/1/297/19072713565_be3113bc67_n.jpg' },
    { image: 'http://c1.staticflickr.com/1/536/19072713515_5961d52357_n.jpg' },
    { image: 'http://c4.staticflickr.com/4/3937/19072713775_156a560e09_n.jpg' },
    { image: 'http://c1.staticflickr.com/1/267/19067097362_14d8ed9389_n.jpg' }
  ];

  $scope.cards = {
    master: Array.prototype.slice.call(cardTypes, 0),
    active: Array.prototype.slice.call(cardTypes, 0),
    discards: [],
    liked: [],
    disliked: []
  }

  $scope.connectToAPI = function(){

    $http({
  method: 'GET',
  url: 'http://htn.toastedsesa.me/api/v1/allprods'
    }).then(function successCallback(response) {
    $scope.products = response.data; 
  

  }, function errorCallback(response) {
    console.log("Fuck");
  });

  }

  $scope.cardDestroyed = function(index) {
    $scope.cards.active.splice(index, 1);
  };

  $scope.addCard = function() {
    var newCard = cardTypes[0];
    $scope.cards.active.push(angular.extend({}, newCard));
  }

  $scope.refreshCards = function() {
    // Set $scope.cards to null so that directive reloads
    $scope.cards.active = null;
    $timeout(function() {
      $scope.cards.active = Array.prototype.slice.call($scope.cards.master, 0);
    });
  }

  $scope.$on('removeCard', function(event, element, card) {
    var discarded = $scope.cards.master.splice($scope.cards.master.indexOf(card), 1);
    $scope.cards.discards.push(discarded);
  });

  $scope.cardSwipedLeft = function(index) {
    console.log('LEFT SWIPE');
    var card = $scope.cards.active[index];
    $scope.cards.active.splice(index, 1);
  };
  $scope.cardSwipedRight = function(index) {
    console.log('RIGHT SWIPE');
    var card = $scope.cards.active[index];
    <!--$scope.cards.liked.push(card);-->
    $scope.cards.active.splice(index, 1);
  };

  $scope.connectToAPI();

})

.controller('CardCtrl', function($scope, TDCardDelegate) {

})

.controller('ChatDetailCtrl', function($scope, $stateParams, Chats) {
  $scope.chat = Chats.get($stateParams.chatId);
})

.controller('AccountCtrl', function($scope) {
  $scope.settings = {
    enableFriends: true
  };
})

.controller('LandingCtrl', function($scope) {
  $scope.settings = {
    enableFriends: true
  };
});
