$.fn.formToJson=function(){form=$(this);var formArray=form.serializeArray(),jsonOutput={};return $.each(formArray,(function(i,element){var elemNameSplit=element.name.split("["),elemObjName="jsonOutput";$.each(elemNameSplit,(function(nameKey,value){nameKey!=elemNameSplit.length-1?(elemObjName="]"==value.slice(value.length-1)?"]"===value?elemObjName+"["+Object.keys(eval(elemObjName)).length+"]":elemObjName+"["+value:elemObjName+"."+value,void 0===eval(elemObjName)&&eval(elemObjName+" = {};")):"]"==value.slice(value.length-1)?"]"===value?eval(elemObjName+"["+Object.keys(eval(elemObjName)).length+"] = '"+element.value.replace("'","\\'")+"';"):eval(elemObjName+"["+value+" = '"+element.value.replace("'","\\'")+"';"):eval(elemObjName+"."+value+" = '"+element.value.replace("'","\\'")+"';")}))})),jsonOutput};


$(document).ready(function(){

    var addButton = $('#add_button');
    var wrapper = $('#studentForm');
    var button_grp = $('#btn_grp');
    var fieldHTML = '<div class="row"><div class="col"><div class="form-group"><label>Field name</label><input type="text" name="field_name[]" value="" class="form-control"/></div></div><div class="col"><div class="form-group"><label>Field value</label><input type="text" name="field_value[]" value="" class="form-control"/></div></div>';

    $(addButton).click(function(){

            $(wrapper).append(fieldHTML);
            $(wrapper).append(button_grp);
    });
});
