function openModalCorfimPrinted(object){
    
    parent = $(object).parent();
    
    tr = $(parent).parent();

    idImpressao = $(parent).children(".id_impressao")[0].value;
    nomeImpressao = $(tr).children(".nome_impressao")[0].innerHTML;

    $("#cod_text_in_modal").html(idImpressao);
    $("#arquivo_text_in_modal").html(nomeImpressao);
    $("#id_impressao_modal").val(idImpressao);

}

function fillDetailsModalData(object){

    parent = $(object).parent();
    tr = $(parent).parent();

    td_data = $(tr).children(".dados_impressao")[0];

    comentario = $(td_data).children(".impressao_comentario")[0].value;
    turma = $(td_data).children(".impressao_turma")[0].value;
    filename = $(td_data).children(".nome_impressao")[0].value;
    cliente = $(td_data).children(".cliente_nome")[0].value;
    data_pedido =  $(td_data).children(".data_pedido")[0].value;

    console.log(comentario, turma, filename, cliente, data_pedido);


    $("#filename_details_modal").html(filename);
    $("#data_pedido_details_modal").html(data_pedido);
    $("#cliente_details_modal").html(cliente);
    $("#turma_details_modal").html(turma);
    $("#comentario_details_modal").html(comentario);
}
