app.controller('eqController', function($scope, $http) {
    // create a message to display in our view
    $http.get('/get/eqdata')
   .then(
       function(response){
         $scope.eq_data = response.data
       }, 
       function(response){
         $scope.eq_data = 'None'
       }
    );
});