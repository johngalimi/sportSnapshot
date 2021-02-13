import React, { useEffect, useState, useCallback } from "react";

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
  Tag,
} from "antd";
import { SearchOutlined } from "@ant-design/icons";

const { Header, Footer, Content } = Layout;
const { Option } = Select;

const App = () => {
  const [isSearchDisabled, setIsSearchDisabled] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [league, setLeague] = useState(null);
  const [season, setSeason] = useState(null);
  const [team, setTeam] = useState(null);
  const [tableData, setTableData] = useState(null);
  const [isDrawerVisible, setIsDrawerVisible] = useState(false);
  const [drawerData, setDrawerData] = useState(null);

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
      });

    setIsLoading(false);
  });

  const getDrawerData = (team) => {
    setTeam(team);
    setIsLoading(true);

    wretch(
      `http://localhost:5000/games?league=${league}&season=${season}&team=${team}`
    )
      .get()
      .json((json) => {
        setDrawerData(json);
      });

    setIsLoading(false);
    setIsDrawerVisible(true);
  };

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
      title: "Games",
      key: "games",
      dataIndex: "games",
      render: (_, record) => (
        <button onClick={() => getDrawerData(record.team_abbr)}>explore</button>
      ),
    },
  ];

  const drawerColumns = [
    {
      title: "Date",
      dataIndex: "game_date",
      key: "game_date",
    },
    {
      title: "",
      dataIndex: "is_team_home",
      key: "is_team_home",
      render: (_, record) => (
        <Tag color={!record.is_team_home && "red"}>
          {record.is_team_home ? "home" : "away"}
        </Tag>
      ),
    },
    {
      title: "Opponent",
      dataIndex: "opponent",
      key: "opponent",
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
          />
        </Drawer>
      </Content>
      <Footer></Footer>
    </Layout>
  );
};

export default App;
