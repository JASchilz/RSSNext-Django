
        var app = angular.module('app', ['restangular', 'ngRoute', 'ngCookies']);

            app.filter( 'domain', function () {
                return function ( input ) {
                  var matches,
                      output = "",
                      urls = /\w+:\/\/([\w|\.]+)/;

                  matches = urls.exec( input );

                  if ( matches !== null ) output = matches[1];

                  return output;
              };
            });

            app.config(function(RestangularProvider) {
                RestangularProvider.setBaseUrl('/v1');
                RestangularProvider.setRequestSuffix('/');

                RestangularProvider.setFullRequestInterceptor(function(element, operation, route, url, headers, params, httpConfig, $cookies) {


                    headers['X-CSRFToken'] = readCookie('csrftoken');

                    return {
                        element: element,
                        params:  params,
                        headers: headers,
                        httpConfig: httpConfig
                    };
                });

                // add a response intereceptor
                RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
                    var extractedData;

                    if (operation === "getList") {
                        extractedData = data.results;
                        extractedData.meta = data;
                    } else {
                        extractedData = data;
                    }
                    return extractedData;
                });

                RestangularProvider.setErrorInterceptor(function(response, deferred, responseHandler) {
                    if(response.status === 400) {
                        angular.forEach(response.data, function(errors, field) {
                          angular.forEach(errors, function(key, value) {
                              make_alert("Error (" + field + "): " + key)

                            });

                        });

                        return false; // error handled
                    }
                    if(response.status === 404) {
                        make_alert("Error: Item not found. Try refreshing the page or hitting the back button.");

                        return false; // error handled
                    }
                    if(response.status === 403 && response.data["detail"] == "Maximum subscriptions reached.") {
                        if(response.data["is_premium"] == 0) {
                            make_alert('Error: Maximum subscriptions reached. <a href="/accounts/premium">Click here</a> to upgrade your account to premium and subscribe to up to 200 feeds.');
                        } else {
                            make_alert("Error: Maximum subscriptions reached.");
                        }


                        return false; // error handled
                    }

                    return true; // error not handled
                });
            });
            app.config(function ($routeProvider, $locationProvider) {
                  $routeProvider
                      .when('/subscriptions',
                          {
                              controller: 'IndexCtrl',
                              templateUrl: '/static/rssnext/partials/index_view.html'
                          })
                      .when('/subscriptions/:subscriptionId',
                          {
                              controller: 'DetailCtrl',
                              templateUrl: '/static/rssnext/partials/detail_view.html'
                          })
                      .otherwise({ redirectTo: '/subscriptions'});

                  $locationProvider.html5Mode(true);
            });



        app.controller('IndexCtrl', function($scope, Restangular, $cookies) {
            $scope.subscriptions = Restangular.all('subscriptions').getList().$object;

            $scope.addSubscription = function() {
                Restangular.all('subscriptions').post({url: $scope.feed_url}).then(function(result) {
                    var subscription = Restangular.restangularizeElement('subscriptions', result);
                    subscription.route = "subscriptions";
                    subscription.parentResource = null;

                    $scope.subscriptions.push(subscription);
                    $scope.feed_url = "";
                })
            };

            $scope.delete = function(subscription) {
                console.log(subscription);
                subscription.remove({csrfmiddlewaretoken: $cookies.csrftoken}).then(function() {
                    var index = $scope.subscriptions.indexOf(subscription);
                    if (index > -1) $scope.subscriptions.splice(index, 1);
                    $location.path( "/" );
                });
            };
        });

        app.controller('DetailCtrl', function($scope, Restangular, $routeParams, $cookies, $location) {
            $scope.subscription = Restangular.one('subscriptions', $routeParams.subscriptionId).get().$object;

            $scope.delete = function(subscription) {
                subscription.remove({csrfmiddlewaretoken: $cookies.csrftoken}).then(function() {
                    $location.path( "/" );
                });
            };
        });