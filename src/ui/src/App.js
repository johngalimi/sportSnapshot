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
  List,
  Avatar,
} from "antd";
import {
  SearchOutlined,
  RightOutlined,
  RiseOutlined,
  SignalFilled,
} from "@ant-design/icons";

const { Header, Footer, Content } = Layout;
const { Option } = Select;
const { Text } = Typography;

const APP_NAME = "SportSnapshot";

window.document.title = APP_NAME;

const App = () => {
  const [isSearchDisabled, setIsSearchDisabled] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [league, setLeague] = useState(null);
  const [season, setSeason] = useState(null);
  const [tableData, setTableData] = useState(null);
  const [isDrawerVisible, setIsDrawerVisible] = useState(false);
  const [drawerData, setDrawerData] = useState(null);
  const [
    isHistoricalPerformanceModalOpen,
    setIsHistoricalPerformanceModalOpen,
  ] = useState(false);
  const [historicalPerformanceData, setHistoricalPerformanceData] = useState(
    []
  );

  useEffect(() => {
    if (league && season) {
      setIsSearchDisabled(false);
    }
  });

  const getTableData = useCallback(() => {
    setIsLoading(true);

    wretch(
      `http://localhost:5000/league_performance?league=${league}&season=${season}`
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

  const handleModalClose = () => setIsHistoricalPerformanceModalOpen(false);

  const getHistoricalTeamPerformance = (team) => {
    setIsLoading(true);

    wretch(
      `http://localhost:5000/team_performance?league=${league}&season=${season}&team=${team}`
    )
      .get()
      .json((json) => {
        setHistoricalPerformanceData(json);
      });

    setIsHistoricalPerformanceModalOpen(true);

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
          <Card title={APP_NAME}>
            <Card type="inner" title="Getting Started">
              Select a league + season and hit search!
            </Card>
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
          visible={isHistoricalPerformanceModalOpen}
          footer={null}
          width={500}
          onCancel={handleModalClose}
        >
          <List
            itemLayout="horizontal"
            dataSource={historicalPerformanceData}
            renderItem={(item) => (
              <List.Item>
                <List.Item.Meta
                  avatar={<Avatar icon={<SignalFilled />} />}
                  title={item.season}
                  description={`${item.wins}-${item.losses}-${item.ot_losses}`}
                />
              </List.Item>
            )}
          />
        </Modal>
      </Content>
      <Footer></Footer>
    </Layout>
  );
};

export default App;
