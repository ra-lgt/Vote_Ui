let fv, offCanvasEl;
async function handleSearchVoters(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  let data = {};

  for (const [key, value] of formData.entries()) {
    data[key] = value;
  }

  const api_url = await fetch(
    `http://127.0.0.1:8081/search_voter?search_string=${data.search_string}&type=${data.choices}`
  );
  const api_res = await api_url.json();
  console.log(api_res)
  document.getElementById('assembly_no').innerHTML=`Assembly No: ${api_res?.data[0]?.assembly_no}`
  document.getElementById('assembly_name').innerHTML=`Assembly Name: ${api_res?.data[0]?.assemblyname}`

  $('.datatables-basic').DataTable().destroy();

  var t;
  $(function () {
    o = {

        'Yes': {
          title: "Voted",
          class: " bg-label-success",
        },
        'No': {
          title: "Not Voted",
          class: " bg-label-danger",
        },
      };
    var l,
      t,
      e = $(".datatables-basic"),
      r =
        (e.length &&
          ((l = e.DataTable({
            data: api_res?.data,
            columns: [
              {
                data: "",
              },
              {
                data: "first_name",
              },
              {
                data: "sex",
              },
              {
                data: "age",
              },
              {
                data: "house_no",
              },
              {
                data: "village",
              },
              {
                data: "vcardid",
              },
              {
                data: "address",
              },
              {
                data: "booth_no",
              },
              {
                data: "boothaddress",
              },
              {
                data: "voted",
              },

            ],
            columnDefs: [
              {
                className: "control",
                orderable: !1,
                searchable: !1,
                responsivePriority: 2,
                targets: 0,
                render: function (e, t, a, s) {
                  return "";
                },
              },

              {
                targets: 1,
                responsivePriority: 4,
                render: function (e, t, a, s) {
                  var n = a.avatar,
                    l = a.first_name,
                    r = a.middle_name;
                  return (
                    '<div class="d-flex justify-content-start align-items-center user-name"><div class="avatar-wrapper"><div class="avatar me-2">' +
                    (n
                      ? '<img src="' +
                        assetsPath +
                        "img/avatars/" +
                        n +
                        '" alt="Avatar" class="rounded-circle">'
                      : '<span class="avatar-initial rounded-circle bg-label-' +
                        [
                          "success",
                          "danger",
                          "warning",
                          "info",
                          "dark",
                          "primary",
                          "secondary",
                        ][Math.floor(6 * Math.random())] +
                        '">' +
                        (n = (
                          ((n =
                            (l = a.first_name).match(/\b\w/g) || []).shift() ||
                            "") + (n.pop() || "")
                        ).toUpperCase()) +
                        "</span>") +
                    '</div></div><div class="d-flex flex-column"><span class="emp_name text-truncate">' +
                    l +
                    '</span> <small class="emp_post text-truncate text-muted"> Middle Name :' +
                    r +
                    "</small> <small class='emp_post text-truncate text-muted'>Last Name :"+ a.last_name+"</small> </div></div>"
                  );
                },
              },
              {
                responsivePriority: 1,
                targets: 4,
              },
              {
                targets: -2,
                render: function (e, t, a, s) {
                  var a = a.age,
                    n = {
                      1: {
                        title: "Current",
                        class: "bg-label-primary",
                      },
                      2: {
                        title: "Professional",
                        class: " bg-label-success",
                      },
                      3: {
                        title: "Rejected",
                        class: " bg-label-danger",
                      },
                      4: {
                        title: "Resigned",
                        class: " bg-label-warning",
                      },
                      5: {
                        title: "Applied",
                        class: " bg-label-info",
                      },
                    };
                  return void 0 === n[a]
                    ? e
                    : '<span class="badge ' +
                        n[a].class +
                        '">' +
                        n[a].title +
                        "</span>";
                },
              },
              {
                targets: -1,
                render: function (e, t, a, s) {
                  var a = a.voted,
                    n = {

                      'Yes': {
                        title: "Voted",
                        class: " bg-label-success",
                      },
                      'No': {
                        title: "Not Voted",
                        class: " bg-label-danger",
                      },
                    };
                  return void 0 === n[a]
                    ? e
                    : '<span class="badge ' +
                        n[a].class +
                        '">' +
                        n[a].title +
                        "</span>";
                },
              },
            ],

            language: {
              paginate: {
                next: '<i class="bx bx-chevron-right bx-18px"></i>',
                previous: '<i class="bx bx-chevron-left bx-18px"></i>',
              },
            },

            responsive: {
              details: {
                display: $.fn.dataTable.Responsive.display.modal({
                  header: function (e) {
                    return "Details of " + e.data().first_name;
                  },
                }),
                type: "column",
                renderer: function (e, t, a) {
                  a = $.map(a, function (e, t) {
                    return "" !== e.title
                      ? '<tr data-dt-row="' +
                          e.rowIndex +
                          '" data-dt-column="' +
                          e.columnIndex +
                          '"><td>' +
                          e.title +
                          ":</td> <td>" +
                          e.data +
                          "</td></tr>"
                      : "";
                  }).join("");
                  return !!a && $('<table class="table"/><tbody />').append(a);
                },
              },
            },
            initComplete: function () {
                this.api()
                  .columns(-1)
                  .every(function () {
                    var e = this,
                      s = $(
                        '<select id="ProductStatus" class="form-select text-capitalize"><option value="">Vote Status</option></select>'
                      )
                        .appendTo(".product_status")
                        .on("change", function () {
                          var t = $.fn.dataTable.util.escapeRegex($(this).val());
                          e.search(t ? "^" + t + "$" : "", !0, !1).draw();
                        });
                    e.data()
                      .unique()
                      .sort()
                      .each(function (t, e) {
                        s.append(
                          '<option value="' +
                            o[t].title +
                            '">' +
                            o[t].title +
                            "</option>"
                        );
                      });
                      $('#ProductStatus').select2();
                  }),

                  this.api()
                    .columns(2)
                    .every(function () {
                      var e = this,
                        s = $(
                          '<select id="ProductCategory" class="form-select text-capitalize"><option value="">Sex</option></select>'
                        )
                          .appendTo(".product_category")
                          .on("change", function () {
                            var t = $.fn.dataTable.util.escapeRegex($(this).val());
                            e.search(t ? "^" + t + "$" : "", !0, !1).draw();
        
                          });
                      e.data()
                        .unique()
                        .sort()
                        .each(function (t, e) {
                          console.log(t,e)

                          s.append(
                            '<option value="' +
                              t +
                              '">' +
                              t +
                              "</option>"
                          );
                        });
                        $('#ProductCategory').select2();
                    }),
                  this.api()
                    .columns(-3)
                    .every(function () {
                      var e = this,
                        s = $(
                          '<select id="ProductStock" class="form-select text-capitalize"><option value=""> Booth No </option></select>'
                        )
                          .appendTo(".product_stock")
                          .on("change", function () {
                            var t = $.fn.dataTable.util.escapeRegex($(this).val());
                            e.search(t ? "^" + t + "$" : "", !0, !1).draw();
                          });
                      e.data()
                        .unique()
                        .sort()
                        .each(function (t, e) {
        
                          s.append(
                            '<option value="' +
                              t +
                              '">' +
                              t +
                              "</option>"
                          );
                        });
                        $('#ProductStock').select2();
                    });
              },
          })),
          $(".dataTables_length").addClass("mt-0 mt-md-3 me-3")));
          
    setTimeout(() => {
      $(".dataTables_filter .form-control").removeClass("form-control-sm"),
        $(".dataTables_length .form-select").removeClass("form-select-sm");
    }, 300);
  });
}
