var ID=0;
var myDiagram;
var DEBUG=false;
var tree;

function genId(){
  return ID++;
}
function centerRoot(scale) {
  myDiagram.scale = scale;
  myDiagram.commandHandler.scrollToPart(myDiagram.findNodeForKey(1));
}
function init() {

  // $(".right").keyup(function(e) {
  //   var code;
  //   if (!e) var e = window.event; // some browsers don't pass e, so get it from the window
  //   if (e.keyCode) code = e.keyCode; // some browsers use e.keyCode
  //   else if (e.which) code = e.which;  // others use e.which
  //   console.log(e.key)
  //   console.log(e.keyCode)
  //   if (code == 46){
  //     console.log("DELETE")
  //     return false;
  //   }
    
// });
  
  // console.log(tree);
  var G = go.GraphObject.make;  // for conciseness in defining templates
  
  myDiagram =
    G(go.Diagram, "myDiagramDiv", // must be the ID or reference to div
      {
        maxSelectionCount: 1, // users can select only one part at a time
        validCycle: go.Diagram.CycleDestinationTree, // make sure users can only create trees
        "clickCreatingTool.insertPart": function(loc) {  // scroll to the new node
          var node = go.ClickCreatingTool.prototype.insertPart.call(this, loc);
          if (node !== null) {
            this.diagram.select(node);
            this.diagram.commandHandler.scrollToPart(node);
            this.diagram.commandHandler.editTextBlock(node.findObject("NAMETB"));
          }
          return node;
        },
        layout:
          G(go.TreeLayout,
            {
              treeStyle: go.TreeLayout.StyleLastParents,
              arrangement: go.TreeLayout.ArrangementHorizontal,
              // properties for most of the tree:
              angle: 90,
              layerSpacing: 35,
              // properties for the "last parents":
              alternateAngle: 90,
              alternateLayerSpacing: 35,
              alternateAlignment: go.TreeLayout.AlignmentBus,
              alternateNodeSpacing: 20,
            }),
        "undoManager.isEnabled": false, // enable undo & redo
        "toolManager.mouseWheelBehavior": go.ToolManager.WheelZoom,
        "draggingTool.dragsTree": true,  // dragging for both move and copy
        "allowDelete":false,             // disable delete elements (replaced with another)
        "allowCopy":false,               // disable coping elements
        "allowMove":true,                // to move nodes arounds 
        "allowSelect":true              
      });

  // when the document is modified, add a "*" to the title and enable the "Save" button
  // myDiagram.addDiagramListener("Modified", function(e) {
  //   var button = document.getElementById("SaveButton");
  //   if (button) button.disabled = !myDiagram.isModified;
  //   var idx = document.title.indexOf("*");
  //   if (myDiagram.isModified) {
  //     if (idx < 0) document.title += "*";
  //   } else {
  //     if (idx >= 0) document.title = document.title.substr(0, idx);
  //   }
  // });

  // manage boss info manually when a node or link is deleted from the diagram
  // myDiagram.addDiagramListener("SelectionDeleting", function(e) {
  //   var part = e.subject.first(); // e.subject is the myDiagram.selection collection,
  //   // so we'll get the first since we know we only have one selection
  //   myDiagram.startTransaction("clear boss");
  //   if (part instanceof go.Node) {
  //     var it = part.findTreeChildrenNodes(); // find all child nodes
  //     while (it.next()) { // now iterate through them and clear out the boss information
  //       var child = it.value;
  //       var bossText = child.findObject("boss"); // since the boss TextBlock is named, we can access it by name
  //       if (bossText === null) return;
  //       bossText.text = "";
  //     }
  //   } else if (part instanceof go.Link) {
  //     var child = part.toNode;
  //     var bossText = child.findObject("boss"); // since the boss TextBlock is named, we can access it by name
  //     if (bossText === null) return;
  //     bossText.text = "";
  //   }
  //   myDiagram.commitTransaction("clear boss");
  // });

  var levelColors = ["#AC193D", "#2672EC", "#8C0095", "#5133AB",
    "#008299", "#D24726", "#008A00", "#094AB2"];

  // override TreeLayout.commitNodes to also modify the background brush based on the tree depth level
  myDiagram.layout.commitNodes = function() {
    go.TreeLayout.prototype.commitNodes.call(myDiagram.layout);  // do the standard behavior
    // then go through all of the vertexes and set their corresponding node's Shape.fill
    // to a brush dependent on the TreeVertex.level value
    myDiagram.layout.network.vertexes.each(function(v) {
      if (v.node) {
        var level = v.level % (levelColors.length);
        var color = levelColors[level];
        var shape = v.node.findObject("SHAPE");
        if (shape) shape.stroke = G(go.Brush, "Linear", { 0: color, 1: go.Brush.lightenBy(color, 0.05), start: go.Spot.Left, end: go.Spot.Right });
      }
    });
  };

  // when a node is double-clicked, add a child to it
  function nodeDoubleClick(e, obj) {
    console.log("docuble click");
    var clicked = obj.part;
    if (clicked !== null) {
      var thisemp = clicked.data;
      myDiagram.startTransaction("add employee");
      var newemp = {
        name: "(new person)",
        title: "",
        comments: "",
        parent: thisemp.key
      };
      myDiagram.model.addNodeData(newemp);
      myDiagram.commitTransaction("add employee");
    }
  }
  
  // this is used to determine feedback during drags
  function mayWorkFor(node1, node2) {
    if (!(node1 instanceof go.Node)) return false;  // must be a Node
    if (node1 === node2) return false;  // cannot work for yourself
    if (node2.isInTreeOf(node1)) return false;  // cannot work for someone who works for you
    return true;
  }

  // This function provides a common style for most of the TextBlocks.
  // Some of these values may be overridden in a particular TextBlock.
  function textStyle() {
    return { font: "9pt  Segoe UI,sans-serif", stroke: "white" };
  }

  // This converter is used by the Picture.
  function findHeadShot(key) {
    if (key < 0 || key > 16) return "images/HSnopic.jpg"; // There are only 16 images on the server
    return "images/HS" + key + ".jpg"
  }

  // define the Node template
  myDiagram.nodeTemplate =
    G(go.Node, "Auto",
      { click: nodeClick},
      // { // handle dragging a Node onto a Node to (maybe) change the reporting relationship
      //   mouseDragEnter: function(e, node, prev) {
      //     var diagram = node.diagram;
      //     var selnode = diagram.selection.first();
      //     if (!mayWorkFor(selnode, node)) return;
      //     var shape = node.findObject("SHAPE");
      //     if (shape) {
      //       shape._prevFill = shape.fill;  // remember the original brush
      //       shape.fill = "darkred";
      //     }
      //   },
      //   mouseDragLeave: function(e, node, next) {
      //     var shape = node.findObject("SHAPE");
      //     if (shape && shape._prevFill) {
      //       shape.fill = shape._prevFill;  // restore the original brush
      //     }
      //   },
      //   mouseDrop: function(e, node) {
      //     var diagram = node.diagram;
      //     var selnode = diagram.selection.first();  // assume just one Node in selection
      //     if (mayWorkFor(selnode, node)) {
      //       // find any existing link into the selected node
      //       var link = selnode.findTreeParentLink();
      //       if (link !== null) {  // reconnect any existing link
      //         link.fromNode = node;
      //       } else {  // else create a new link
      //         diagram.toolManager.linkingTool.insertLink(node, node.port, selnode, selnode.port);
      //       }
      //     }
      //   }
      // },
      // for sorting, have the Node.text be the data.name
      new go.Binding("text", "name"),
      // bind the Part.layerName to control the Node's layer depending on whether it isSelected
      new go.Binding("layerName", "isSelected", function(sel) {return sel ? "Foreground" : ""; }).ofObject(),
      // define the node's outer shape
      G(go.Shape, "Rectangle",
        {
          name: "SHAPE", fill: "#333333", stroke: 'white', strokeWidth: 3.5,
          // set the port properties:
          portId: "", fromLinkable: false, toLinkable: false, cursor: "pointer"
        }),
      G(go.Panel, "Horizontal",
        // define the panel where the text will appear
        G(go.Panel, "Table",
          {
            minSize: new go.Size(130, NaN),
            maxSize: new go.Size(150, NaN),
            margin: new go.Margin(10, 10, 10, 10),
            defaultAlignment: go.Spot.Center
          },
          G(go.RowColumnDefinition, { column: 1, width: 4 }),
          G(go.TextBlock, textStyle(),  // the name
            {
              row: 0, column: 0, columnSpan: 5,
              font: "12pt Segoe UI,sans-serif",
              editable: false, isMultiline: false,
              minSize: new go.Size(10, 16), cursor: "pointer"
            },
            new go.Binding("text", "name").makeTwoWay())
          
        )  // end Table Panel
      ) // end Horizontal Panel
    );  // end Node

  // the context menu allows users to make a position vacant,
  // remove a role and reassign the subtree, or remove a department
  myDiagram.nodeTemplate.contextMenu =
    G("ContextMenu",
      // G("ContextMenuButton",
      //   G(go.TextBlock, "Vacate Position"),
      //   {
      //     click: function(e, obj) {
      //       var node = obj.part.adornedPart;
      //       if (node !== null) {
      //         var thisemp = node.data;
      //         myDiagram.startTransaction("vacate");
      //         // update the key, name, and comments
      //         myDiagram.model.setDataProperty(thisemp, "name", "(Vacant)");
      //         myDiagram.model.setDataProperty(thisemp, "comments", "");
      //         myDiagram.commitTransaction("vacate");
      //       }
      //     }
      //   }
      // ),
      // G("ContextMenuButton",
      //   G(go.TextBlock, "Remove Role"),
      //   {
      //     click: function(e, obj) {
      //       // reparent the subtree to this node's boss, then remove the node
      //       var node = obj.part.adornedPart;
      //       if (node !== null) {
      //         myDiagram.startTransaction("reparent remove");
      //         var chl = node.findTreeChildrenNodes();
      //         // iterate through the children and set their parent key to our selected node's parent key
      //         while (chl.next()) {
      //           var emp = chl.value;
      //           myDiagram.model.setParentKeyForNodeData(emp.data, node.findTreeParentNode().data.key);
      //         }
      //         // and now remove the selected node itself
      //         myDiagram.model.removeNodeData(node.data);
      //         myDiagram.commitTransaction("reparent remove");
      //       }
      //     }
      //   }
      // ),
      // G("ContextMenuButton",
      //   G(go.TextBlock, "Remove Department"),
      //   {
      //     click: function(e, obj) {
      //       // remove the whole subtree, including the node itself
      //       var node = obj.part.adornedPart;
      //       if (node !== null) {
      //         myDiagram.startTransaction("remove dept");
      //         myDiagram.removeParts(node.findTreeParts());
      //         myDiagram.commitTransaction("remove dept");
      //       }
      //     }
      //   }
      // )
      // function nodeDoubleClick(e, obj) {
      //   console.log("docuble click");
      //   var clicked = obj.part;
      //   if (clicked !== null) {
      //     var thisemp = clicked.data;
      //     myDiagram.startTransaction("add employee");
      //     var newemp = {
      //       name: "(new person)",
      //       title: "",
      //       comments: "",
      //       parent: thisemp.key
      //     };
      //     myDiagram.model.addNodeData(newemp);
      //     myDiagram.commitTransaction("add employee");
      //   }
      // }
      G("ContextMenuButton",
        G(go.TextBlock, " Ajouter un fils "),
        {
          click: function(e, obj) {
            // remove the whole subtree, including the node itself
            var node = obj.part.adornedPart;
            if (node !== null) {
              var thisNode = node.data;
              var newNode = {
                name: "",
                tag: thisNode['tag']+'>',
                parent: thisNode.key,
                action:"None",
                config:[],
                context:"",
                keywords:[],
                next:[],
                text:[]
              };
              myDiagram.model.addNodeData(newNode);
            }
          }
        }
      ),
      G("ContextMenuButton",
        G(go.TextBlock, " Supprimer "),
        {
          click: function(e, obj) {
            // remove the whole subtree, including the node itself
            var node = obj.part.adornedPart;
            if (node !== null) {
              Fnon.Ask.Danger(
                "Êtes-vous sûr de vouloir supprimer definitivement cette branche de l'arbre",
                'Attention !!!','Oui', 'Non', 
                (result)=>{
                if (result){
                  var thisNode = node.data;
                  let myTree =JSON.parse(JSON.stringify(tree));
                  let partTree = getTreeByTag(tree,thisNode['tag'])[0];
                  if (partTree!=undefined){
                    let listTagNext = TreeToListTag(partTree);
                    myTree = removeNode(myTree,thisNode,listTagNext);
                    sendTree(myTree,()=>{   // callback if success
                      load();
                    },()=>{                 // callback if fail

                    });
                  }else{
                    myDiagram.removeParts(node.findTreeParts());
                  }
                  $("#form-container").replaceWith('<div id="form-container"></div>')
                }
              });
              
            }
          }
        }
      )
    );

  // define the Link template
  myDiagram.linkTemplate =
    G(go.Link, go.Link.Orthogonal,
      { corner: 5, relinkableFrom: false, relinkableTo: false },
      G(go.Shape, { strokeWidth: 1.5, stroke: "#F5F5F5" }));  // the link shape

  // read in the JSON-format data from the "mySavedModel" element
  load();
  // myDiagram.commandHandler.zoomToFit();
  
  // zoomToFit();

  // support editing the properties of the selected person in HTML
  if (window.Inspector) myInspector = new Inspector("myInspector", myDiagram,
    {
      properties: {
        "key": { readOnly: true },
        "comments": {}
      }
    });

  // Setup zoom to fit button
  function zoomToFit() {
    myDiagram.commandHandler.zoomToFit();
  }

  


} // end init

  function TreeToModel(tree){
    myTree =JSON.parse(JSON.stringify(tree));
    let listTag= TreeToListTag(myTree);
    let tagKey = {};
    listTag.forEach((tag,index) => tagKey[tag]=index)
    // let listNode = TreeToListNode(tree,tagKey);
    // console.log(listNode);
    let model = { 
      "class": "go.TreeModel",
      "nodeDataArray": TreeToListNode(myTree,tagKey)
    }

    return model

  }

  function TreeToListTag(tree){
    if (typeof tree == "string"){
      return [];
    }
    else{
      let list = [];
      list.push(tree['tag']);
      tree['next'].forEach(next => {list = list.concat(TreeToListTag(next));});
      return list;
    }
  }

  function TreeToListNode(tree,tagKey,parent=0){
    if (typeof tree == "string"){
      return [];
    }
    else{
      let list = [];
      tree["key"]=tagKey[tree['tag']];
      tree["parent"]=parent;
      tree["name"] = tree['tag'].split('>')[tree['tag'].split('>').length -1].toUpperCase();
      list.push(tree);
      // if (tree["tag"] == "start") console.log(`TreeToList(${tree['tag']},${key},${parent})`);
      // let list_next=[];
      // tree['next'].forEach((next,index) => {if (typeof next != "string") list_next.push(next)});
      tree['next'].forEach((next,index) => {
        // console.log(`TreeToList(${next['tag']},${key+index+1},${key}) | index: ${index}`);
        list = list.concat(TreeToListNode(next,tagKey,tree["key"]));
      });
      return list;
    }
  }

  // function addKeyToTree(tree,listNode,parent=0){
  //   if (typeof tree == "string"){
  //     return [];
  //   }
  //   else{
  //     let i=0;
  //     while (tree['tag']!=listNode[i]['tag']){
  //       i++;
  //     }
  //     tree['key']=i;
  //     tree['parent']=parent;
  //     let list = [];
  //     list.push(tree);
  //     tree['next'].forEach((next,index) => {list = list.concat(TreeToList(next));});
  //     return list;
  //   }
  // }

  
  // Show the diagram's model in JSON format
  // function save() {
  //   document.getElementById("mySavedModel").value = myDiagram.model.toJson();
  //   myDiagram.isModified = false;
  // }
  
  function load() {
    // model={ "class": "go.TreeModel",
    // "nodeDataArray":TreeToList(tree)
    // }
    // console.log(model)
    $.ajax({
      type:"POST",
      url:"/get_tree",
      datatype:"json",
      success: (data)=>{
        tree = data['tree'] 
        model = TreeToModel(tree);
        // console.log(model)
        myDiagram.model = go.Model.fromJson(model);
        // make sure new data keys are unique positive integers
        var lastkey = 1;
        myDiagram.model.makeUniqueKeyFunction = function(model, data) {
          var k = data.key || lastkey;
          while (model.findNodeDataForKey(k)) k++;
          data.key = lastkey = k;
          return k;
        };

        centerRoot(.7);
      }
    }).fail(printError);          //envoyer un message d'error si la requête a échoué
    
  }
  window.addEventListener('DOMContentLoaded', init);
  
function nodeClick(e, obj){
  var clicked = obj.part;
  if (clicked !== null) {
    var node = clicked.data;
    genForm(node);
    
  }
}

function genForm(node){
  let listTag = TreeToListTag(tree);
  let html=`
    <div id="form-container">

      

      <form id="form" onsubmit="update();return false">

        <div id="form-header" class="sticky">
          <div id="label-tag">${formatTag(node['tag'],spacing=true)}</div>
          <input id="original-tag" type="hidden" value="${node['tag']}">
          <input type="submit" value="Enregistrer">
          <div id="deco-header"></div>
        </div>

        <div id="inputs-container">
          <div class="form-element">
            <label> Nom : &ensp; </label>
            <span data-tooltip="${info['name']}"><span class="material-icons-outlined info-icon" >info</span></span>
            <br>
            <input pattern="^[^<>]+$" id="input-name" type="text" value="${node['tag'].split('>')[node['tag'].split('>').length -1]}" autocomplete="off" required>
            
          </div>

          <div class="form-element"> 
            <label>Mots Clés : &ensp; </label>
            <span data-tooltip="${info['keywords']}"><span class="material-icons-outlined info-icon" >info</span></span>
            <input id="input-keywords" type="text" data-role="taginput" data-tag-separator="|||" data-tag-trigger="Enter" value="${node['keywords'].join('|||')}">
          </div>

          <div class="form-element">
            <label>Action : &ensp;</label>
            <span data-tooltip="${info['action']}"><span class="material-icons-outlined info-icon" >info</span></span>
            <br>
            <input id="input-action" type="text" value="${node['action']!="None"?node['action']:""}" autocomplete="off">
          </div>

          <div class="form-element">
          <input id="input-screen" type="checkbox" ${node['config'].includes('screen')?"checked":""}>
          <label id="label-screen" for="input-screen" for>Besoin d'écran ?</label>
          <span data-tooltip="${info['screen']}"><span class="material-icons-outlined info-icon" >info</span></span>
          </div>


          <div class="form-element">
            <label> Text : &ensp;</label>
            <span id="add-text" class="add clickable-icon material-icons add-icon">add</span>
            <span data-tooltip="${info['text']}">&ensp;&ensp;<span class="material-icons-outlined info-icon" >info</span></span>
            <br>
            <fieldset >
              <div id="list-text">
                ${(()=>{
                  let html="";
                  node['text'].forEach(listText => {
                    html+= `
                      <p class="text-section">
                        <input id="input-text-${genId()}" class="input-text " type="text" data-role="taginput" data-tag-separator="|||" data-tag-trigger="Enter" value="${listText.join('|||')}" required>
                        <span class="delete-text"><span class="clickable-icon material-icons delete-icon delete-icon-text">delete</span></span>
                      </p>
                    `
                  });
                  return html;
                })()}
              </div>
            </fieldset>
          </div>


          <div class="form-element">
            <label>Redirection :  &ensp; </label>
            <span data-tooltip="${info['next']}"><span class="material-icons-outlined info-icon" >info</span></span>
            <select name="next-nodes" id="next-nodes">
              <option value="">--Please choose an option--</option>
              ${(()=>{
                let html="";
                listTag.forEach(tag=>{
                  html+= `<option value="${tag}">${tag}</option>`
                });
                return html;
              })()}
            </select>
            <div id="list-next-nodes">
              ${(()=>{
                let html="";
                node['next'].forEach(next=>{
                  if (typeof next=="string")
                    html+=`<p class="next" value="${next}"><span class="next-span">${next}</span><span class="delete-next"><span class="clickable-icon material-icons delete-icon delete-icon-next">delete</span></span></p>`
                });
                return html;
              })()}
            </div>
          </div>



          
          <div id="test" style="background:red;cursor:pointer;display:${DEBUG?"block":"none"}">Test</div>
        </div>

      </form>

    </div>
        
  `;


  $('#form-container').replaceWith(html);
  addEventsForm();
}

function addEventsForm(){

  $("#inputs-container").css('margin-top',document.getElementById('form-header').offsetHeight);

  $('select').selectize({
    sortField: 'text'
  });
  
  $('#add-text').click(()=>{
    $('#list-text').append(`
      <p class="text-section">
        <input id="input-text-${genId()}" class="input-text" type="text" data-role="taginput" data-tag-separator="|||" data-tag-trigger="Enter">
        <span class="delete-text"><span class="clickable-icon material-icons delete-icon delete-icon-text">delete</span></span>
      </p>
    `);

    $('.delete-text').click(function(){$(this).parent()[0].remove();});

  });

  $('.delete-text').click(function(){$(this).parent()[0].remove();});

  $('#input-name').keyup(function(){
    let name = $(this).val();
    let tag = formatTag($("#label-tag").text(),spacing=false);
    let newTag = tag.substr(0,tag.lastIndexOf(">")+1)+name;
    $("#label-tag").text(formatTag(newTag,spacing=true));
    $("#inputs-container").css('margin-top',document.getElementById('form-header').offsetHeight);

  });

  $("#next-nodes").change(function(){
    if ($("#next-nodes").val()!=""){
      $("#list-next-nodes").append(`<p class="next" value="${$("#next-nodes").val()}"><span class="next-span">${$("#next-nodes").val()}</span><span class="delete-next"><span class="clickable-icon material-icons delete-icon delete-icon-next">delete</span></span></p>`);
      $('.delete-next').click(function(){$(this).parent()[0].remove();});
    }
  });

  $('.delete-next').click(function(){$(this).parent()[0].remove();});

  $('[data-toggle="tooltip"]').tooltip();

  
  $('#test').click(update);
}

function update(){
  node={
    originalTag:$("#original-tag").val().trim(),
    tag:formatTag($("#label-tag").text(),spacing=false).trim(),
    name:$("#input-name").val().trim(),
    keywords:$('#input-keywords').data('taginput').val(),
    action: $('#input-action').val()==""?"None":$('#input-action').val().trim(),
    config:$('#input-screen').is(":checked")?["screen"]:[],
    text:(()=>{
      let listText = [];
      $('.input-text .original-input').each((index,input) => {
        let taginput=$('#'+input.id).data('taginput').val();
        if (taginput.length>0)
          listText.push(taginput);
      });
      return listText;
    })(),
    next:(()=>{
      let listNext = [];
      $('.next').each((index,obj) => {
        let next = obj.getAttribute("value");
        if (!listNext.includes(next))
          listNext.push(next);
      });
      return listNext;
    })()
  }  
  
  // send new tree
  let myTree = JSON.parse(JSON.stringify(tree));
  myTree = updateTree(myTree,node);
  sendTree(myTree,()=>{      // callback if success
    // update graph
    load();
    genForm(node);
  },()=>{                    // callback if fail

  });
  
}
function updateTree(tree,node){
  let listTag = TreeToListTag(tree);
  if (listTag.includes(node['originalTag']))
    tree = modifyTree(tree,node);
  else
    tree = modifyTree(tree,node,true);

  return tree
}

function modifyTree(tree,node,newNode=false){
  if (typeof tree == "string"){
    if (tree==node['originalTag'])
      return node['tag'];
    return tree;
  }
  else{
    if (newNode){
      
      // console.log(node['originalTag']==tree['tag']);

      if(node['originalTag'].substr(0, node['originalTag'].length - 1)==tree['tag']){
        // console.log("added")
        next = {
          tag: node['tag'],
          action: node['action'],
          config: node['config'],
          context: "",
          keywords :node['keywords'],
          next: [],
          text: node['text'],
          next: node['next']
        }
        tree['next'].push(next);

      }

      tree['next'].forEach((next,index,listNext)=> listNext[index]= modifyTree(next,node,newNode));

      return tree

    }
    else{
      if(node['originalTag']==tree['tag']){

        tree['tag'] = node['tag']
        tree['keywords'] = node['keywords']
        tree['action'] = node['action']
        tree['config'] = node['config']
        tree['text'] = node['text']  

        let listNext= tree['next'].filter(next => typeof next != "string");
        listNext = listNext.concat(node['next']);
        tree['next'] = listNext;

      }
      tree['next'].forEach((next,index,listNext)=> listNext[index]= modifyTree(next,node,newNode));

      return tree

    } 
  }
}

function removeNode(tree,node,listNextTag){
  if (typeof tree == "string"){
    if (listNextTag.includes(tree))
      return undefined;
    return tree;
  }
  else{
    if(node['tag']==tree['tag']){
      return undefined;
    }
    else{
      let listNext = [];
      tree['next'].forEach((next,index)=> {
        let n = removeNode(next,node,listNextTag);
        if (n!= undefined){
          listNext.push(n);
        }
      });
      tree['next'] = listNext;
    }

    return tree
  }

    
}


function getTreeByTag(tree,tag){
  if (typeof tree != "string"){
    if (tree['tag']==tag){
      return [tree];
    }
    else{
      let l = [];
      tree['next'].forEach(next=> {
        l = l.concat(getTreeByTag(next,tag));
      });
      return l
    }
  }
  return [];
  
}

function sendTree(tree,callbackSuccess,callbackFail){
  $.ajax({
    type:"POST",
    url:'/send_tree',
    contentType: "application/json;charset=UTF-8",
    data: JSON.stringify({'tree':tree}),
    success: (response)=>{
      if (response == "success"){
        Fnon.Hint.Success("Succès de la mise à jour",{
          position:"right-bottom",
          fontSize: '16px',
          animationDuration: 500,
          displayDuration: 2000,
          progressColor: 'rgba(255,255,255,0)',
          callback:function(){}
        }); 
        callbackSuccess();
      }
    }
  }).fail( (error)=>{
    console.log(error);
    Fnon.Hint.Danger("Une erreur s'est produite", {
      position:"right-bottom",
      fontSize: '16px',
      animationDuration: 500,
      displayDuration: 3000,
      progressColor: 'rgba(255,255,255,0)',
      callback:function(){}
    });  
    callbackFail();
    
  });  

}

function genInfoBox(title){
  let html= 
    `<span class="tooltip-toggle" data-toggle="tooltip" title="${title}" tabindex="0">
      <svg viewBox="0 0 27 27" xmlns="http://www.w3.org/2000/svg"><g fill="#ED3E44" fill-rule="evenodd"><path d="M13.5 27C20.956 27 27 20.956 27 13.5S20.956 0 13.5 0 0 6.044 0 13.5 6.044 27 13.5 27zm0-2C7.15 25 2 19.85 2 13.5S7.15 2 13.5 2 25 7.15 25 13.5 19.85 25 13.5 25z"/><path d="M12.05 7.64c0-.228.04-.423.12-.585.077-.163.185-.295.32-.397.138-.102.298-.177.48-.227.184-.048.383-.073.598-.073.203 0 .398.025.584.074.186.05.35.126.488.228.14.102.252.234.336.397.084.162.127.357.127.584 0 .22-.043.412-.127.574-.084.163-.196.297-.336.4-.14.106-.302.185-.488.237-.186.053-.38.08-.584.08-.215 0-.414-.027-.597-.08-.182-.05-.342-.13-.48-.235-.135-.104-.243-.238-.32-.4-.08-.163-.12-.355-.12-.576zm-1.02 11.517c.134 0 .275-.013.424-.04.148-.025.284-.08.41-.16.124-.082.23-.198.313-.35.085-.15.127-.354.127-.61v-5.423c0-.238-.042-.43-.127-.57-.084-.144-.19-.254-.318-.332-.13-.08-.267-.13-.415-.153-.148-.024-.286-.036-.414-.036h-.21v-.95h4.195v7.463c0 .256.043.46.127.61.084.152.19.268.314.35.125.08.263.135.414.16.15.027.29.04.418.04h.21v.95H10.82v-.95h.21z"/></g></svg>
    </span>`;
  return html;
}

function formatTag(tag,spacing=false){
  let newTag = "";
  let list = tag.split('>')

  if (spacing){
    newTag = list.join(" > ")
  }
  else{
    newTag= list.map(Function.prototype.call, String.prototype.trim).join('>')
  }

  return newTag;
}

function printError(error){    //afficher la page d'erreur 
		
  console.error("status: "+error['status']+"\nstatusText: "+error['statusText']);
  $('body').replaceWith(error['responseText']);
  
  }