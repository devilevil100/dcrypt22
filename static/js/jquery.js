
function createAlert(title, summary, details, severity, dismissible, autoDismiss, appendToId, reload=false) {
  var iconMap = {
    info: "fa fa-info-circle",
    success: "fa fa-thumbs-up",
    warning: "fa fa-exclamation-triangle",
    danger: "fa ffa fa-exclamation-circle"
  };

  var iconAdded = false;

  var alertClasses = ["alert", "animated", "flipInX"];
  alertClasses.push("alert-" + severity.toLowerCase());

  if (dismissible) {
    alertClasses.push("alert-dismissible");
  }

  var msgIcon = $("<i />", {
    "class": iconMap[severity] // you need to quote "class" since it's a reserved keyword
  });

  var msg = $("<div />", {
    "class": alertClasses.join(" ") // you need to quote "class" since it's a reserved keyword
  });

  if (title) {
    var msgTitle = $("<h4 />", {
      html: title
    }).appendTo(msg);

    if(!iconAdded){
      msgTitle.prepend(msgIcon);
      iconAdded = true;
    }
  }

  if (summary) {
    var msgSummary = $("<strong />", {
      html: summary
    }).appendTo(msg);

    if(!iconAdded){
      msgSummary.prepend(msgIcon);
      iconAdded = true;
    }
  }

  if (details) {
    var msgDetails = $("<p />", {
      html: details
    }).appendTo(msg);

    if(!iconAdded){
      msgDetails.prepend(msgIcon);
      iconAdded = true;
    }
  }


  if (dismissible) {
    var msgClose = $("<span />", {
      "class": "close", // you need to quote "class" since it's a reserved keyword
      "data-dismiss": "alert",
      html: "<i class='fa fa-times-circle'></i>"
    }).appendTo(msg);
  }

  $('#' + appendToId).prepend(msg);
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if(autoDismiss){
    setTimeout(function(){
      msg.addClass("flipOutX");
      setTimeout(function(){
        msg.remove();
        if(reload){
    window.location.reload()
  }
      },5000);
    }, 5000);
  }
  
}

function submit(){
  $.ajax({
          type: "POST",
          url: "answer/",
          data:{"ans": $("input[name='answer']").val(), csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
          success:function(resp){
            console.log(resp)
    if(resp === "incorrect"){
      if($(".quest")[0].children.length !== 3){
      $("#questioncontext").after('<h3 style="color:red; margin-bottom: 1em;     text-align: center;" id="response" >  Incorrect Answer  </h3>')
      }
      else{
        $("#response").html("Incorrect Again")
      }

    }
    else if(resp === "hack"){

      if($(".quest")[0].children.length !== 3){
      $("#questioncontext").after('<h3 style="color:red; margin-bottom: 1em;     text-align: center;" id="response" >Special character mm? trying to hack. oof  </h3>')
      }
      else{
        $("#response").html("Special character mm? trying to hack. oof")
      }
    }
    else if(resp === "correct"){
      window.location.reload()
    }
  }
       });
}

$(".usemulti").click(function(){
  if (  $("input[name='multi']").val() == "no"){
  $("input[name='multi']").val("yes")
  $(".remainingmulti").html(parseInt($(".remainingmulti").html())-1)
  $(".usemulti").html("Remove")
  }
  else if (  $("input[name='multi']").val() == "yes"){
  $("input[name='multi']").val("no")
  $(".remainingmulti").html(parseInt($(".remainingmulti").html())+1)
  $(".usemulti").html("Use")
  }
})
$("#attack").click(function (){
  if($("input[name='soldiers']").val() === '0' && $("input[name='bombers']").val() === '0' && $("input[name='tanks']").val() === '0'){
    alert("Please select troops to attack")
    return false;
  }
  $.ajax({
          type: "POST",
          url: "/attack/",
          data:{"soldiers": $("input[name='soldiers']").val(),
          "bombers": $("input[name='bombers']").val(),
          "tanks": $("input[name='tanks']").val(),
          "multi": $("input[name='multi']").val(),
          "team": $("#attackingteam").html().split(" ")[1],
           csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
          success:function(resp){
            console.log(resp)
    if(resp === "win"){
      window.location.reload()

    }
    else if(resp === "hack"){

      if($(".quest")[0].children.length !== 3){
      $("#questioncontext").after('<h3 style="color:red; margin-bottom: 1em;     text-align: center;" id="response" >Special character mm? trying to hack. oof  </h3>')
      }
      else{
        $("#response").html("Special character mm? trying to hack. oof")
      }
    }
    else if(resp === "lose"){
      window.location.reload()
    }
  }
       });
})
$('.poison').click(function (){
console.log(this.parentNode.parentNode.children[4].value)
var teamname = this.parentNode.parentNode.children[4].value
$.ajax({
        type: "POST",
        url: "/poison/",
        data:{"teamname": teamname,

        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
        success:function(resp){
          console.log(resp)
  if(resp === "hack"){


    createAlert('','Nice Try','Well seems like you tried to change the input values or scripts. A moderator would be contacting you soon :)','danger',true,true,'leaderboard');

  }
  else if(resp === "poisoned"){
    window.location.reload()

  }
}
     });
})
function buytroops(){
  console.log('g')
  $.ajax({
          type: "POST",
          url: "/buytroops/",
          data:{"soldiers": $("input[name='soldiers']").val(),
          "bombers": $("input[name='bombers']").val(),
          "tanks": $("input[name='tanks']").val(),
          "aag": $("input[name='aag']").val(),
          'multiplier': $("input[name='multiplier']").val(),
          'shield': $("input[name='shield']").val(),
          'hp': $("input[name='hp']").val(),
          'poison': $("input[name='poison']").val(),
          'bonusfp': $("input[name='bonusfp']").val(),
          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
          success:function(resp){
            console.log(resp)
    if(resp === "hack"){


      createAlert('','Nice Try','Well seems like you tried to change the input values or scripts. A moderator would be contacting you soon :)','danger',true,true,'shopp');

    }
    else if(resp === "bought"){
      window.location.reload()

    }
  }
       });
}
function gotoquestion(ques){
  $.ajax({
          type: "POST",
          url: "/question/",
          data:{"ques": ques, csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
          success:function(){
    location.reload()
  }
       });
}
