$(function(){
    $("startSearch").click(function(){
        $.getJSON("/query", function(result){
          $.each(result, function(i, field){
            var name = i.split('/').pop.replace("_", " ").split('.')[0]
            var div = document.createElement('div');
            div.setAttribute('class', 'gallery');

            var a = document.createElement('a');
            a.setAttribute('target', 'blank');
            a.setAttribute('href', i);
            
            var img = document.createElement('img');
            img.setAttribute('src', i);
            img.setAttribute('width', '600');
            img.setAttribute('height', '600');
            
            a.appendChild(img);
            div.appendChild(a);
            
            var desc = document.createElement('div');
            desc.setAttribute('class', 'desc');
            desc.innerHTML = name;

            div.appendChild(desc);

            $("image_results").append(div);
          });
        });
      });
})

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