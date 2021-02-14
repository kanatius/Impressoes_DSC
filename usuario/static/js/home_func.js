function openModalCorfimPrinted(object){
    
    parent = $(object).parent();
    
    tr = $(parent).parent();

    idImpressao = $(parent).children(".id_impressao")[0].value;
    nomeImpressao = $(tr).children(".nome_impressao")[0].innerHTML;

    $("#cod_text_in_modal").html(idImpressao);
    $("#arquivo_text_in_modal").html(nomeImpressao);
    $("#id_impressao_modal").val(idImpressao);

}