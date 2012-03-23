// ToDO
/*

    Autocomplete family names
    Improve search algorithm (iterating over everything is not exactly light..)
    Specify search terms    
    Add more fields to database

*/

        function paint_nodes(devdata, devdata_2){
            var rels="", processed_relationships=Array();
            $('#nodes').prepend('() ');
            $.each(devdata, function(id, relationships){ 
                $.each(relationships, function(key, rel) {
                    if (jQuery.inArray(rel, processed_relationships) == -1){ 
                        rels += "( "+rel+":"+devdata_2[rel]+") ";;
                        processed_relationships.push(rel); 
                    }
                 });
                $('#nodes').append( "(" + devdata_2[id] + " > [" + relationships.join(',') +  "] )" );
            });

            $('#nodes').append(' || ' + rels + "\n");
            $('#nodes').addClass('arrows-and-boxes');
            $('#nodes').arrows_and_boxes();
        }

        var devdata={}, devdata_2={};
        $(function() { 

            $.ajax({
                url: '/RPC/',
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify ({jsonrpc:'2.0', method:'get_or_create_task', params:['Genealogy'], id:'jsonrpc', }),
                success: function (result){ result=result.result;
                    console.debug(result);
                    var user = result[0], job = result[1], work = result[2], task = result[3];
                    console.debug([user, job, work, task]);
                    $.ajax({
                       url: '/RPC/', 
                       data: JSON.stringify ({jsonrpc:'2.0',
                           method:'send_command',
                           params:[ user, job, work, task, 'get_node_names', ''],
                           id:"jsonrpc"} ),  // id is needed !!
                       type:"POST",
                       dataType:"json",
                       success:  function (data_2){
                          devdata_2=data_2; 
                          $.ajax({
                              url: '/RPC/', 
                              data: JSON.stringify ({jsonrpc:'2.0',
                                  method:'send_command',
                                  params:[ user, job, work, task, 'get_parent_nodes', ''],
                                  id:"jsonrpc"} ),  // id is needed !!
                             type:"POST",
                             dataType:"json",
                             success:  function (data)       { 
                                console.debug(data); console.debug(data_2);
                                 paint_nodes(data.result, data_2.result);
                             },
                             error: function (err)  { alert ("Error");}
                          });
                       },
                       error: function (err)  { alert ("Error");}
                    }); }
                });
         });

    function create_personality(data){ // Create a personality based on the data provided by the user.
            $.ajax({
                url: '/RPC/',
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify ({jsonrpc:'2.0', method:'create_identity', params:[data], id:'jsonrpc', }),
                success: function (result){ result=result.result; }
            });
        return result;
    

    function get_possible_identities(id, data){ // user_id familiar_data
            $.ajax({
                url: '/RPC/',
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify ({jsonrpc:'2.0', method:'get_possible_identities', params:[id, data], id:'jsonrpc', }),
                success: function (result){ result=result.result; }
            });
        return result;
    }

    function process_identity(data){
        res = "<ul class='person'>"
        $(data).each(function(element){ res +="<li class=\'" + element[0] + "\'>" + element[1] + "</li>"; });
        return res + "</ul>"
    }
