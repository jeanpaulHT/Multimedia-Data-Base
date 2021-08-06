$(function(){
    $('startSearch').click(function() {
        var img = $(Upload).val();
        $.ajax({
            url: '/',
            data: img,
            dataType: 'img',
            success: function(data){
                results = document.getElementById('results');
                results.innerHTML = "";
            }
        })
    }

    )
})