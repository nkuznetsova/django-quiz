$(document).ready(function() {
    // The maximum number of answers
    var MAX_OPTIONS = 10;
    //var MAX_NUM_ANSWER = 0;

    $('#QuestionForm')
        // Add button click handler
        .on('click', '.addButton', function() {
            var $template = $('#answerTemplate'),
                $clone    = $template
                                .clone()
                                .removeClass('hide')
                                .removeAttr('id')
                                .insertBefore($template);
                $answer   = $clone.find('[name="newanswer_"]');
                $answer.prop('required',true);
                $iscorrect = $clone.find('[name="newiscorrect_"]');
                NEXT_NUM_ANSWER = ($(':visible[name^=newanswer]').length);
                $answer.attr("name", "newanswer_" + NEXT_NUM_ANSWER);
                $iscorrect.attr("name", "newiscorrect_" + NEXT_NUM_ANSWER);

            // Add new field
            //$('#QuestionForm').bootstrapValidator('addField', $answer);
        })

        // Remove button click handler
        .on('click', '.removeButton', function() {
            var $row    = $(this).parents('.answer-group');
                //$answer = $row.find('[name="answer"]');

            // Remove element containing the option
            $row.remove();

            // Remove field
            //$('#QuestionForm').bootstrapValidator('removeField', $answer);
        })

        // Called after adding new field
        .on('added.field.bv', function(e, data) {
            // data.field   --> The field name
            // data.element --> The new field element
            // data.options --> The new field options

            if (data.field === 'answer') {
                if ($('#QuestionForm').find(':visible[class="answer-group"]').length >= MAX_OPTIONS) {
                    $('#QuestionForm').find('.addButton').attr('disabled', 'disabled');
                }
            }
        })

        // Called after removing the field
        .on('removed.field.bv', function(e, data) {
           if (data.field === 'answer') {
                if ($('#QuestionForm').find(':visible[class="answer-group"]').length < MAX_OPTIONS) {
                    $('#QuestionForm').find('.addButton').removeAttr('disabled');
                }
            }
        });

     $('#TestForm')
        .on('click', '.addQuestion', function() {
            var $template = $('#answerTemplate'),
                $clone    = $template
                                .clone()
                                .removeClass('hide')
                                .removeAttr('id')
                                .insertBefore($template);
                $answer   = $clone.find('[name="newanswer_"]');
                $answer.prop('required',true);
                $iscorrect = $clone.find('[name="newiscorrect_"]');
                NEXT_NUM_ANSWER = ($(':visible[name^=newanswer]').length);
                $answer.attr("name", "newanswer_" + NEXT_NUM_ANSWER);
                $iscorrect.attr("name", "newiscorrect_" + NEXT_NUM_ANSWER);

            // Add new field
            //$('#QuestionForm').bootstrapValidator('addField', $answer);
        })
});
