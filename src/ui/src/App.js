import React, { useEffect, useState } from "react";

import { seasonData } from "./mockData.js";

import range from "underscore/modules/range.js";

import "antd/dist/antd.css";
import { Layout, Table, Select, Space, Tooltip, Button, Card } from "antd";
import { SearchOutlined } from "@ant-design/icons";

const { Header, Footer, Content } = Layout;
const { Option } = Select;

const seasonColumns = [
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
];

const App = () => {
  const [isSearchDisabled, setIsSearchDisabled] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [league, setLeague] = useState(null);
  const [season, setSeason] = useState(null);
  const [tableData, setTableData] = useState(seasonData);

  useEffect(() => {
    if (league && season) {
      setIsSearchDisabled(false);
    }
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
            />
          </Tooltip>
        </Space>
      </Header>
      <Content>
        {tableData ? (
          <Table
            columns={seasonColumns}
            // dataSource={seasonData}
            dataSource={tableData}
            rowKey="team"
            size="middle"
            pagination={{ pageSize: 12 }}
          />
        ) : (
          <Card title="No filters selected">
            <p>Please select a league and season to continue</p>
          </Card>
        )}
      </Content>
      <Footer></Footer>
    </Layout>
  );
};

export default App;
