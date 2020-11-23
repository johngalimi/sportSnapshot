import "./App.css";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

const createGameRecord = (
  league,
  season,
  date,
  team,
  opponent,
  teamPoints,
  opponentPoints
) => {
  return { league, season, date, team, opponent, teamPoints, opponentPoints };
};

const columnNames = [
  "League",
  "Season",
  "Date",
  "Team",
  "Opponent",
  "Team Points",
  "Opponent Points",
];

const gameRecords = [
  createGameRecord(
    "NHL",
    "2017-18",
    "2017-10-05",
    "Boston Bruins",
    "Nashville Predators",
    4,
    3
  ),
  createGameRecord(
    "NHL",
    "2017-18",
    "2017-10-09",
    "Boston Bruins",
    "Colorado Avalanche",
    0,
    4
  ),
];

function App() {
  const classes = useStyles();

  return (
    <div className="App">
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableHead>
            <TableRow>
              {columnNames.map((column, idx) => {
                return <TableCell key={idx}>{column}</TableCell>;
              })}
            </TableRow>
          </TableHead>
          <TableBody>
            {
              gameRecords.map((game, idx) => {
                return <TableRow key={idx}>
                  {
                    Object.keys(game).map((datum, idx) => {
                      return <TableCell key={idx}>{game[datum]}</TableCell>
                    })
                  }
                </TableRow>
              })
            }
          </TableBody>
        </Table>
      </TableContainer>
    </div >
  );
}

export default App;
