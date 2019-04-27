$("#searchButton").click(function (e) {
  e.preventDefault();
  $.ajax({
      type: "GET",
      url: '/imageSearch/searchResults',
      data: {
        'imageToSearch': ""
      },
      success: function (data) {
         for (imageName in data['resultImageNames']) {
            var result = "<li>" + '<img src= "https://s3-us-west-1.amazonaws.com/flickrbigdatacu/'+data['resultImageNames'][imageName]+'">' + "</li>";
            $("#resultImages").append(result); 
          }
      }
    });

  });

