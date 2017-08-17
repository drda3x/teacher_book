(function () {
    "use strict";
    
    function joinArray(arr) {
        var result = [];

        for(var i=0, j=arr.length; i<j; i++) {
            var cur = arr[i];
            result.push(cur);

            if(cur.groups.length > 1) {
                result = result.concat(cur.groups);
            }
        }

        return result
    }

    window.pageInit = function(data, groups) {
        app.controller("AdminListCtrl", ["$scope", function($scope) {
            $scope.data = data;
            $scope.groups = groups;

            $scope.row = null;
            $scope.rowClick = function(index, event) {
                $scope.blockEvent(event);
                $scope.row = index;
                $scope.contextMenu.close();
            }

            $scope.addRow = function(event) {
                $scope.blockEvent(event);
                $scope.data.push({
                    student: {
                        first_name: null,
                        last_name: null,
                        phone: null 
                    },
                    groups : []
                });

                $scope.rowClick($scope.data.length - 1, event);
            }

            $scope.blockEvent = function(event) {
                event.preventDefault();
                event.stopPropagation();
            }

            $scope.checkTable = function() {
                var result = [];

                for(var i=0, j=$scope.data.length; i<j; i++) {
                    var st = $scope.data[i].student,
                        gr = $scope.data[i].groups;
                    
                    var filled = st.first_name && st.first_name && st.phone;
                    if (filled || gr.length > 0) {
                        result.push($scope.data[i]);
                    }
                }

                $scope.data = result;
            }

            $scope.contextMenu = {
                show: false,
                event: null,
                record: null,
                items: [],

                open: function(record, event) {
                    this.show = true;
                    this.event = event;
                    this.record = record;
                },

                close: function() {
                    this.show = false;
                }
            }

            $scope.contextMenu.items = [
                {
                    label: 'Перевести', 
                    callback: $.proxy(function() {
                        this.show = false;
                        $scope.moveModal.open(this.record);
                    }, $scope.contextMenu) 
                },{
                    label: 'Удалить',
                    callback: $.proxy(function() {
                        this.show = false;
                        if(confirm("Удалить ученика из списков?")) {
                            alert("Функция не реализована!!!");
                        }
                    }, $scope.contextMenu)
                }
            ];

            $scope.moveModal = {
                show: false,
                data: null,

                open: function(data) {
                    this.data = data;
                    this.show = true;
                },
                
                close: function() {
                    this.show = false;
                },

                toggle: function() {
                    this.show = !this.show;
                },

                save: function(group) {
                    var stid = this.data.student.id,
                        gid = group.id;
                }
            }

            $('body').click(function() {
                $scope.$apply(function() {
                    $scope.row = null;
                    $scope.checkTable();
                });
            });
        }])
    }
})();
