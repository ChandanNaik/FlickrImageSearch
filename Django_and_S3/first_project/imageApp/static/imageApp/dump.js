$("#dumpButton").click(function (e) {
  console.log("Dumping......")
  e.preventDefault();
  $.ajax({
      type: "GET",
      url: '/imageSearch/performDump',
      success: function (data) {
            console.log("Dump successfully completed.");
      }
    });

  });

