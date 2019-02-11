/*HIGHSCORE SUBMIT AND RETRIEVE*/

  /*Submit new score to the DB using AJAX*/

  $(function()
  {
    var form = $('#scoreboard-form');
    $(form).submit(function(event) {
      event.preventDefault();
      var enteredName = document.getElementById("playersName").value;
      $.ajax({
        url: "overview_score.py",
        type: "post",
        datatype: "json",
        data: {'highScore': totalScore, 'name': enteredName},
        success: function(response){
          innerModule=document.getElementById("scoreboard-message");
          text='<br><p>Thank you for submitting!<br>Your current rank: '+response+'</p><br>'
          button='<button class="btn btn-default" onclick="restartGame()">Beat your score</button>'
          innerModule.innerHTML=text+button;
        }
      })
    });
  });
