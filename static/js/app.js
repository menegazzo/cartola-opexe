var app = angular.module("BlankApp", ["ngMaterial"]);

app.config(["$interpolateProvider", function ($interpolateProvider) {
  $interpolateProvider.startSymbol("{[");
  $interpolateProvider.endSymbol("]}");
}]);

app.controller("timesCtrl", ["$scope", "$http", "$q", function($scope, $http, $q) {

  $scope.orderBy = undefined;
  $scope.open = 0;
  $scope.times = [];
  
  $scope.getStyle = function (index) {
    // Prize zone
    if (index < 3) {
      return {"color": "blue"};
    }
    
    // Barbecue zone
    if (index >= $scope.times.length - 4) {
      return {"color": "red"};
    }
    
    // Michel"s bitches zone
    var times = $scope.times.map(function (item, index) {
      return item["time_id"];
    });
    if (index > times.indexOf(3438309)) {
      return {"color": "orange"};
    }
  };

  var statusPromise = $http.get("/status/").then(function (status) {
    $scope.open = status.data["open"];
  });
  
  var teamsPromise = $q.when(statusPromise, function () {
    return $http.get("/times/").then(function (times) {
      $scope.times = times.data;
    });
  });
  
  var partialsPromise = $q.when(teamsPromise, function () {
    if ($scope.open === true) {
      return $q.reject("Mercado aberto");
    }
    
    var promises = [];
    angular.forEach($scope.times, function (time) {
      promises.push($http.get("/times/" + time["slug"] + "/parciais/"));
    });
    return $q.all(promises);
  });
  
  $q.when(partialsPromise, function (parciais) {
    angular.forEach(parciais, function (parcial, index) {
      var time = $scope.times[index];
      var parcial_total = parcial.data["total"];
      time["pontos"]["parcial"] = parcial_total;
      time["pontos"]["campeonato"] += parcial_total;
      time["jogaram"] = parcial.data["jogaram"];
    });
    $scope.orderBy = "-pontos.parcial";
  });

}]);