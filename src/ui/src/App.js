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
  Modal,
  Typography,
} from "antd";
import { Line } from "@ant-design/charts";
import { SearchOutlined, RightOutlined, RiseOutlined } from "@ant-design/icons";

const { Header, Footer, Content } = Layout;
const { Option } = Select;
const { Text } = Typography;

const data = [
  { season: "2010", wins: 3 },
  { season: "2011", wins: 4 },
  { season: "2012", wins: 3.5 },
  { season: "2013", wins: 5 },
  { season: "2014", wins: 4.9 },
  { season: "2015", wins: 6 },
  { season: "2016", wins: 7 },
  { season: "2017", winse: 9 },
];
const config = {
  data,
  height: 400,
  xField: "season",
  yField: "wins",
  point: {
    size: 5,
    shape: "diamond",
  },
  label: {
    style: {
      fill: "#aaa",
    },
  },
};

const App = () => {
  const [isSearchDisabled, setIsSearchDisabled] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [league, setLeague] = useState(null);
  const [season, setSeason] = useState(null);
  const [tableData, setTableData] = useState(null);
  const [isDrawerVisible, setIsDrawerVisible] = useState(false);
  const [drawerData, setDrawerData] = useState(null);
  const [isGraphModalOpen, setIsGraphModalOpen] = useState(false);

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

  const handleModalClose = () => setIsGraphModalOpen(false);

  const getHistoricalTeamPerformance = (team) => {
    setIsLoading(true);

    console.log(team);

    setIsGraphModalOpen(true);

    setIsLoading(false);
  };

  const tableColumns = [
    {
      title: "Team",
      dataIndex: "team",
      key: "team",
      align: "left",
      width: 250,
      render: (text, record) => (
        <Space>
          <Tooltip
            title="historical performance"
            placement="bottomRight"
            arrowPointAtCenter
          >
            <Button
              size="small"
              shape="round"
              icon={<RiseOutlined />}
              onClick={() => getHistoricalTeamPerformance(record.team_abbr)}
            />
          </Tooltip>
          <Text strong>{text}</Text>
        </Space>
      ),
    },
    {
      title: "W",
      dataIndex: "wins",
      key: "wins",
      align: "center",
    },
    {
      title: "L",
      dataIndex: "losses",
      key: "losses",
      align: "center",
    },
    {
      title: "OTL",
      dataIndex: "ot_losses",
      key: "ot_losses",
      align: "center",
    },
    {
      title: "Games",
      key: "games",
      dataIndex: "games",
      render: (_, record) => (
        <Button
          type="primary"
          size="small"
          shape="round"
          icon={<RightOutlined />}
          onClick={() => getDrawerData(record.team_abbr)}
        >
          view
        </Button>
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
        <Modal
          visible={isGraphModalOpen}
          footer={null}
          width={1000}
          onCancel={handleModalClose}
        >
          <Line {...config} />
        </Modal>
      </Content>
      <Footer></Footer>
    </Layout>
  );
};

export default App;
