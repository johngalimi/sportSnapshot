import React, { useEffect, useState, useCallback } from "react";

import { gameData } from "./mockData.js";

import range from "underscore/modules/range.js";

import wretch from "wretch";

import "antd/dist/antd.css";
import {
  Layout,
  Table,
  Select,
  Space,
  Tooltip,
  Button,
  Card,
  Drawer,
} from "antd";
import { SearchOutlined } from "@ant-design/icons";

const { Header, Footer, Content } = Layout;
const { Option } = Select;

const tableColumns = [
  {
    title: "Team",
    dataIndex: "team",
    key: "team",
    width: 200,
  },
  {
    title: "W",
    dataIndex: "wins",
    key: "wins",
    width: 50,
  },
  {
    title: "L",
    dataIndex: "losses",
    key: "losses",
    width: 50,
  },
  {
    title: "OTL",
    dataIndex: "ot_losses",
    key: "ot_losses",
    width: 50,
  },
  {
    title: "OTL",
    dataIndex: "ot_losses",
    key: "ot_losses",
    width: 50,
  },
];

const drawerColumns = [
  {
    title: "Date",
    dataIndex: "date",
    key: "date",
  },
  {
    title: "Opponent",
    dataIndex: "opponent",
    key: "opponent",
  },
  {
    title: "",
    dataIndex: "is_home",
    key: "is_home",
  },
  {
    title: "PF",
    dataIndex: "team_points",
    key: "team_points",
  },
  {
    title: "PA",
    dataIndex: "opponent_points",
    key: "opponent_points",
  },
];

const App = () => {
  const [isSearchDisabled, setIsSearchDisabled] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [league, setLeague] = useState(null);
  const [season, setSeason] = useState(null);
  const [tableData, setTableData] = useState(null);
  const [isDrawerVisible, setIsDrawerVisible] = useState(true);
  // const [drawerData, setDrawerData] = useState(null);
  const [drawerData, setDrawerData] = useState(gameData);

  useEffect(() => {
    if (league && season) {
      setIsSearchDisabled(false);
    }
  });

  const getTableData = useCallback(() => {
    setIsLoading(true);

    wretch(
      `http://localhost:5000/performance?league=${league}&season=${season}`
    )
      .get()
      .json((json) => {
        setTableData(json);
        // add button using cols array: https://stackoverflow.com/questions/64119052/adding-button-inside-ant-design-table-column
        // setTableData(
        //   json.map((el) => ({
        //     ...el,
        //     render: () => <button>hello</button>,
        //   }))
        // );
      });

    setIsLoading(false);
  });

  const getDrawerData = useCallback(() => {
    setIsLoading(true);

    // wretch(
    //   `http://localhost:5000/performance?league=${league}&season=${season}`
    // )
    //   .get()
    //   .json((json) => {
    //     setTableData(json);
    //   });

    setDrawerData([
      {
        date: "1/2/2010",
        opponent: "Detroit Red Wings",
        team_points: 4,
        opponent_points: 3,
        is_home: true,
      },
    ]);

    setIsLoading(false);
  });

  return (
    <Layout>
      <Header>
        <Space>
          <Select
            style={{ width: 150 }}
            placeholder="League"
            onChange={setLeague}
          >
            {["NHL", "NBA"].map((league, index) => {
              return (
                <Option key={index} value={league}>
                  {league}
                </Option>
              );
            })}
          </Select>
          <Select
            style={{ width: 150 }}
            placeholder="Season"
            onChange={setSeason}
          >
            {range(2019, 2009, -1).map((season, index) => {
              return (
                <Option key={index} value={season}>
                  {season}
                </Option>
              );
            })}
          </Select>
          <Tooltip title="Get Season Performance">
            <Button
              type="primary"
              shape="circle"
              icon={<SearchOutlined />}
              disabled={isSearchDisabled}
              loading={isLoading}
              onClick={getTableData}
            />
          </Tooltip>
        </Space>
      </Header>
      <Content>
        {tableData ? (
          <Table
            columns={tableColumns}
            dataSource={tableData}
            rowKey="team"
            size="middle"
            pagination={{ pageSize: 12 }}
          />
        ) : (
          <Card title="Getting Started">
            <p>Select a league and season and hit search!</p>
          </Card>
        )}
        <Drawer
          width={640}
          visible={isDrawerVisible}
          closable={true}
          onClose={() => setIsDrawerVisible(false)}
        >
          <Table
            columns={drawerColumns}
            dataSource={drawerData}
            rowKey="team"
            size="middle"
            pagination={{ pageSize: 12 }}
          />
        </Drawer>
      </Content>
      <Footer></Footer>
    </Layout>
  );
};

export default App;
