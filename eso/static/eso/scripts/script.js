let app = angular.module('ericaSantosOsteopada', []);

app.controller('mainCtrl', function ($scope, $http, $window) {
    // Variables
    let nav_item_elements = document.querySelectorAll(".nav-item");
    let opinion_elements = document.querySelectorAll(".opinion");
    let active_opinion_element = opinion_elements[0];

    // Functions
    $scope.showNavMenu = function (nav_item_expansive_element) {
        nav_item_expansive_element.classList.add("expanded");
    };

    $scope.hideNavMenu = function (nav_item_expansive_element) {
       nav_item_expansive_element.classList.remove("expanded");
       console.log("triggerring hide")
    };

    $scope.navButtonActivate = function () {
        let dropdown_nav = document.getElementById("nav-menu-expandable");

        if (dropdown_nav.classList.contains("expanded")) {
            $scope.hideNavMenu(dropdown_nav)
        } else {
            $scope.showNavMenu(dropdown_nav);
        }
    };

    $scope.validateAppointmentForm = function () {
        let elem_name = document.getElementById("appointment-form-name");
        let elem_phone = document.getElementById("appointment-form-phone");
        let elem_email = document.getElementById("appointment-form-email");
        let elem_day = document.getElementById("appointment-form-day");
        let elem_month = document.getElementById("appointment-form-month");
        let elem_year = document.getElementById("appointment-form-year");
        let elem_hour = document.getElementById("appointment-form-hour");
        let elem_minutes = document.getElementById("appointment-form-minutes");
        let elem_description = document.getElementById("appointment-form-description");
        let invalid_elements = [];

        if (elem_name.value === "") {
            invalid_elements.push(elem_name);
        }

        if (elem_phone.value === "" || !Number.isInteger(parseInt(elem_phone.value)) || elem_phone.value.length !== 9) {
            invalid_elements.push(elem_phone);
        }

        try {
            if (elem_email.value !== "" && elem_email.value.split("@").length !== 2 && elem_email.value.split("@")[1].split(".").length !== 2) {
            invalid_elements.push(elem_email);
        }
        } catch (error) {
            invalid_elements.push(elem_email);
        }


        if (elem_day.value === "" || !Number.isInteger(parseInt(elem_day.value)) || parseInt(elem_day.value) < 1 || parseInt(elem_day.value) > 31) {
            invalid_elements.push(elem_day)
        }

        if (elem_month.value === "" || !Number.isInteger(parseInt(elem_month.value)) || parseInt(elem_month.value) < 1 || parseInt(elem_month.value) > 12) {
            invalid_elements.push(elem_month)
        }

        if (elem_year.value === "" || !Number.isInteger(parseInt(elem_year.value)) || parseInt(elem_year.value) < new Date().getFullYear() ) {
            invalid_elements.push(elem_year)
        }

        if (elem_hour.value === "" || !Number.isInteger(parseInt(elem_hour.value)) || parseInt(elem_hour.value) > 24) {
            invalid_elements.push(elem_hour)
        }

        if (elem_minutes.value === "" || !Number.isInteger(parseInt(elem_minutes.value)) || parseInt(elem_minutes.value) > 60) {
            invalid_elements.push(elem_minutes)
        }

        if (elem_description.value === "") {
            invalid_elements.push(elem_description);
        }

        if (invalid_elements.length === 0) {
            let data = {"name": elem_name.value,
                        "phone": elem_phone.value,
                        "email": elem_email.value,
                        "day": elem_day.value,
                        "month": elem_month.value,
                        "year": elem_year.value,
                        "hour": elem_hour.value,
                        "minutes": elem_minutes.value,
                        "description": elem_description.value,
                        "form": "appointment"
            };

            let element_response = document.getElementById("request-response-appointment");

            $scope.loading(document.getElementById("appointment-form-button-submit"), element_response);
            $ajaxUtils.sendPostRequest(data, "/marcacoes/", function (response) {
                if (response["status"] === "successful") {
                    element_response.innerHTML = "<div class='response-message'>Pedido de marcação feito com sucesso</div>";
                } else {
                    element_response.innerHTML = "<div class='response-message'>Ocorreu um erro ao fazer o pedido de marcação</div>";
                }
            });
        } else {
            $window.alert("Existem campos inválidos ou vazios");
            $scope.highlightInvalidFields(invalid_elements, [elem_name, elem_phone, elem_email, elem_day, elem_month, elem_year, elem_hour, elem_minutes,
                elem_description]);
        }
    };

    $scope.validateOpinionForm = function() {
        let elem_name = document.getElementById("opinion-form-name");
        let elem_post = document.getElementById("opinion-form-post");
        let invalid_elements = [];

        if (elem_name.value === "") {
            invalid_elements.push(elem_name);
        }

        if (elem_post.value === "") {
            invalid_elements.push(elem_post);
        }

        if (invalid_elements.length === 0) {
            let data = {"name": elem_name.value,
                        "opinion": elem_post.value,
                        "form": "opinion"
            };

            let element_response = document.getElementById("request-response-opinion");

            $scope.loading(document.getElementById("opinion-form-button-submit"), element_response);
            $ajaxUtils.sendPostRequest(data, "/opiniao/", function (response) {
                if (response["status"] === "successful") {
                    element_response.innerHTML = "<div class='response-message'>Opinião submetida com sucesso</div>";
                } else {
                    element_response.innerHTML = "<div class='response-message'>Ocorreu um erro ao submeter a opinião</div>";
                }
            });
        } else {
            $window.alert("Existem campos inválidos ou vazios");
            $scope.highlightInvalidFields(invalid_elements, [elem_name, elem_post]);
        }
    };

    $scope.highlightInvalidFields = function (invalid_elements, all_elements) {
        for (let i=0; i<all_elements.length; i++) {
            // all_elements[i].style.boxShadow = "";
            all_elements[i].style.backgroundColor = "white";
        }

        for (let i=0; i<invalid_elements.length; i++) {
            // invalid_elements[i].style.boxShadow = "0 0 5px rgba(152, 49, 20, 1)";
            invalid_elements[i].style.backgroundColor = "#FFCCCC";
        }
    };

    $scope.returnScrollCoordinateX = function(active_element_index, total_elements, scroll_width, direction) {
        if (direction === 'next') {
          return -active_element_index * scroll_width;
        } else {
          return (-active_element_index + 2) * scroll_width;
        }
    };

    $scope.switchOpinion = function (direction) {
        let opinion_container_element = document.getElementById("opinion-container");
        let scroll_width = opinion_container_element.offsetWidth;
        let active_opinion_index;
        let scroll_coordinate_x;
        let counter = 1;
        for (let i=0; i<opinion_elements.length; i++) {
          if (opinion_elements[i] === active_opinion_element){
              active_opinion_index = counter;
              break
          }
          counter += 1;
        }

        if (direction === "next") {
            angular.element(active_opinion_element).removeClass("opinion-active");

            if (active_opinion_index !== opinion_elements.length) {
                active_opinion_element = active_opinion_element.nextElementSibling;
            } else {
                active_opinion_element = opinion_elements[0];
            }

            angular.element(active_opinion_element).addClass("opinion-active");

            counter = 0;
            for (let i=0; i<opinion_elements.length; i++) {
              if (opinion_elements[i] === active_opinion_element){
                  active_opinion_index = counter;
                  break
              }
              counter += 1;
            }

            scroll_coordinate_x = $scope.returnScrollCoordinateX(active_opinion_index, opinion_elements.length, scroll_width, direction);
            opinion_container_element.scrollTo({top: 0, left: scroll_coordinate_x, behavior: "smooth"});
        }
    };

    $scope.loading = function (element_to_replace, element_response) {
        element_to_replace.remove();
        angular.element(element_response).removeClass("hidden");
    };

    function setActiveOpinion() {
        if (opinion_elements.length > 1) {
            angular.element(opinion_elements[0]).addClass("opinion-active");
            setInterval(function () {$scope.switchOpinion("next")}, 5000);
        }
    }

    // Function Calls
    for (let i=0; i<nav_item_elements.length; i++) {
        if (nav_item_elements[i].classList.contains("nav-item-expansive")) {
          nav_item_elements[i].addEventListener("mouseover", function () {$scope.showNavMenu(nav_item_elements[i])});
          nav_item_elements[i].addEventListener("mouseout", function () {$scope.hideNavMenu(nav_item_elements[i])});
        }
    }

    setActiveOpinion();
    document.getElementById("main-content").addEventListener("click", function () {
        $scope.hideNavMenu(document.getElementById("nav-menu-expandable"))})

});