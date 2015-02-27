
document.getElementById('product_add').onclick = function() {
    alert(this.value);


    $.ajax({
      type: "POST",
      url: "/cart/",
      data: {
          'product_id': 1
      },
      dataType: "text", //пробовал и html
      cashe: false,
      success: function(data) {
        alert('Ok');   
      },
      error: function(data) {
        alert('error');  
      }      
    });
  
};   
    
