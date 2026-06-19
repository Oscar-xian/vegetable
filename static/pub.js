function bindUploadPicture() {
    $("#image-upload").on("change", function(event) {  // ✅ 添加 event
        const file = event.target.files[0];  // ✅ 现在有 event 了
        if (!file) return;

        const formData = new FormData();
        formData.append("picture", file);

        $.ajax({  //
            url: '/upload/picture',
            type: 'POST',  // ✅ 明确指定 POST
            data: formData,
            processData: false,
            contentType: false,
            success: function(result) {
                const category = result['category'];
                const filename = result['filename'];
                console.log(category);
                console.log(filename)

                let imagePreview=$("#image-preview");
                imagePreview.attr("src","/media/"+filename);
                imagePreview.removeClass("hidden");
                $("#image-placeholder").addClass("hidden");
                $("#category").val(category.id);
                $("#picture").val("/media/"+filename);



            },
            error: function(err) {
                console.log('上传失败:', err);
            }
        });
    });
}

$(function() {
    bindUploadPicture();  // ✅ 确保函数被调用
});