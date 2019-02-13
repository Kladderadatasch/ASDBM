$(function()
{
  var totalScore = 100;
  var scoreLine0 = -15;
  var scoreLine1 = -20;
  var scoreLine2 = -30;

  var pointReference0 = scoreLine0,scoreLine1;
  var pointReference1 = scoreLine1,scoreLine2;
  var pointReference2 = scoreLine1,scoreLine3;

  var fromCounter = pointReference0;
  var toCounter = null;

  function() {
    // set onlick the clicked pointReference as
    // toCounter if the point is connected
    // by a line from the fromCounter
  }

  if (fromCounter == pointReference0 && toCounter == pointReference1)
    totalScore = totalScore + scoreLine0 + scoreLine1;
    return totalScore

});
