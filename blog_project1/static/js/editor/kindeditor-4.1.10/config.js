KindEditor.ready(function(K) {
    window.editor = K.create('#id_content',{
        width:'500px',
        height:'200px',
        uploadJson: '/admin/upload/kindeditor',
        });
});
