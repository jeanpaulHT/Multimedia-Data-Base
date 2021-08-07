function loadImage(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      $('#mainresult')
        .attr('src', e.target.result)
        .attr('width', '400')
        .attr('height', '400');
    };
    reader.readAsDataURL(input.files[0]);
  }
}