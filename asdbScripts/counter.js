//insert Event Listener for Classes \n\
//if Statements in this function \n\

      var totalScore = 100;
      var scoreLine0 = -15;
      var scoreLine1 = -20;
      var scoreLine2 = -30;
      var scoreLine3 = -28;
      // var testScore = totalScore + scoreLine0

      var pointReference0 = [document.getElementById("waypoint0"),scoreLine0,scoreLine1];
      var pointReference1 = [document.getElementById("waypoint1"),scoreLine1,scoreLine2];
      var pointReference2 = [document.getElementById("waypoint2"),scoreLine1,scoreLine3];

      var fromCounter = pointReference0;
      var toCounter = null;

      function clickCounter() {
        // set onlick the clicked pointReference as \n\
        // toCounter if the point is connected \n\
        // by a line from the fromCounter \n\

        // also how to resctrict the paths where it's possible to go ---- && !()

        if((this.id == "waypoint1") && !(fromCounter == pointReference1)){
            var toCounter = pointReference1;
            if ((fromCounter == pointReference0) && (toCounter == pointReference1)){
                totalScore = totalScore + scoreLine0 + scoreLine1;
                alert(totalScore);
            }
        }
      }

      $("circle.counter_test").click(clickCounter);
